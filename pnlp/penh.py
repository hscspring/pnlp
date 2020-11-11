import copy
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Tuple, Optional
from itertools import chain

import numpy as np

from .pcut import cut_zhchar, cut_part, psent, psubsent
from .ptxt import Regex
from .stopwords import chinese_stopwords, english_stopwords

reg = Regex()
STOPWORDS = list(english_stopwords | chinese_stopwords)
# 主要对功能词（与实词对应）采样处理
SAMPLE_WORDS = [w for w in STOPWORDS if reg.pwnb.search(w)]
# 副词、介词、连词、助词、其他虚词
SAMPLE_POS = ["d", "p", "c", "u", "xc"]


def swap(lst: list, index: int, start: int, end: int) -> list:
    """Randomly swap two continuous parts."""
    assert start <= index <= end <= len(lst) - 1
    if (index == start or np.random.rand() < 0.5) and index != end:
        lst[index], lst[index+1] = lst[index+1], lst[index]
    else:
        lst[index], lst[index-1] = lst[index-1], lst[index]
    return lst


@dataclass
class Sampler:

    def check_types(self):
        default_types = set(("delete", "swap", "insert"))
        for typ in self.types:
            if typ not in default_types:
                raise ValueError("Type {} is not a valid type.".format(typ))


@dataclass
class TokenLevelSampler(Sampler):

    """
    Random choose an index.
    - Insert a copy token. Usually a function word.
    - Delete a token.
    - Swap with the prev or the next token.

    Parameters
    -------------
    rate: The sampling rate (each type respectively).
    types: Sampling methods. You should take care of the order.
    sample_words: Words will be used in sampling. Usually use stopwords.
    sample_pos: Part-of-speech will be used in sampling. Usually use function pos.

    Note
    ------
    1. We mainly use `stopwords (usually function words)` as sample words to do the sampling.
    If you want to sample other kinds of words, you could appoint `sample_pos` to what you need,
    then your input should include POS flags.
    2. The order of the `types` will influence the output of the dependent_sample.
    """
    rate: float = 0.05
    types: List[str] = field(
        default_factory=lambda: ["delete", "swap", "insert"])
    sample_words: List[str] = field(
        default_factory=lambda: SAMPLE_WORDS)
    sample_pos: List[str] = field(
        default_factory=lambda: SAMPLE_POS)

    def __post_init__(self):
        self.len_types = len(self.types)
        self.check_types()
        assert self.rate <= 0.1

    def filter_sample_idx(
        self,
        token_list: List[str or Tuple[str, str]]
    ) -> List[int]:
        if not token_list:
            return []
        if type(token_list[0]) == str:
            can_deal_idx = [i for (i, w) in enumerate(
                token_list) if w in self.sample_words]
        else:
            can_deal_idx = [i for (i, (w, f)) in enumerate(
                token_list) if f in self.sample_pos]
        return can_deal_idx

    def choose_sample_idx(
        self,
        len_parts: int,
        sample_count: int
    ) -> List[int]:
        size = min(len_parts, sample_count)
        sample_part_idx = np.random.choice(
            len_parts, size, replace=False).tolist()
        return sample_part_idx

    def delete_sampling(
        self,
        token_list: List[str or Tuple[str, str]],
        sample_idx: List[int]
    ) -> List[str or Tuple[str, str]]:
        """Simple delete sampling. Delete the tokens in the given indexes.
        """
        result = []
        for i, token in enumerate(token_list):
            if i in sample_idx:
                continue
            result.append(token)
        return result

    def insert_sampling(
        self,
        token_list: List[str or Tuple[str, str]],
        sample_idx: List[int]
    ) -> List[str or Tuple[str, str]]:
        """Simple insert sampling. Insert the tokens in the given indexes.
        """
        result = []
        for i, token in enumerate(token_list):
            if i in sample_idx:
                result.append(token)
            result.append(token)
        return result

    def swap_sampling(
        self,
        token_list: List[str or Tuple[str, str]],
        sample_idx: List[int]
    ) -> List[str or Tuple[str, str]]:
        """Simple swap sampling. Swap the tokens in the given indexes. 
        DONOT swap start and end.
        """
        result = copy.deepcopy(token_list)
        end = len(token_list) - 1
        for idx in sample_idx:
            swap(result, idx, 0, end)
        return result

    def _sampling(
        self,
        type: str,
        parts:  List[List[str] or List[Tuple[str, str]]],
        sample_idx: List[int]
    ) -> List[List[str] or List[Tuple[str, str]]]:
        """
        Sampling by part, each time deal with a part instead of a token.
        """
        cp_parts = copy.deepcopy(parts)
        for j, part in enumerate(cp_parts):
            if j not in sample_idx:
                continue
            can_deal_idx = self.filter_sample_idx(part)
            if not can_deal_idx:
                continue
            deal_idx = np.random.choice(can_deal_idx, 1).tolist()[0]
            if type == "delete":
                part.remove(part[deal_idx])
            elif type == "insert":
                part.insert(deal_idx, part[deal_idx])
            else:
                swap(part, deal_idx, can_deal_idx[0], can_deal_idx[-1])
        return cp_parts

    def independent_sampling(
        self,
        token_list: List[str or Tuple[str, str]]
    ) -> List[List[str] or List[Tuple[str, str]]]:
        result = []
        parts = self.convert_tokens_to_parts_by_nonword(token_list)
        len_parts = len(parts)
        len_tokens = len(token_list)
        sample_count = round(len_tokens * self.rate) * self.len_types
        sample_count = max(sample_count, 1)
        # 一次采样到位，之后只是分别操作，操作原则上互相不依赖
        sample_part_idx = self.choose_sample_idx(len_parts, sample_count)
        each_count = len(sample_part_idx) // self.len_types

        for i, typ in enumerate(self.types):
            sample_idx = sample_part_idx[i*each_count: (i+1)*each_count]
            new_parts = self._sampling(typ, parts, sample_idx)
            sample = list(chain(*new_parts))
            result.append(sample)
        return result

    def dependent_sampling(
        self,
        token_list: List[str or Tuple[str, str]]
    ) -> List[str or Tuple[str, str]]:
        parts = self.convert_tokens_to_parts_by_nonword(token_list)
        len_parts = len(parts)
        len_tokens = len(token_list)
        sample_count = round(len_tokens * self.rate)
        sample_count = max(sample_count, 1)
        for i, typ in enumerate(self.types):
            # 每次重新采样，后面的操作可能会与前面的操作重叠
            sample_idx = self.choose_sample_idx(len_parts, sample_count)
            parts = self._sampling(typ, parts, sample_idx)
        return list(chain(*parts))

    def convert_tokens_to_parts_by_nonword(
        self,
        token_list: List[str or Tuple[str, str]]
    ) -> List[List[str] or List[Tuple[str, str]]]:
        parts = []
        tmp = []
        for token in token_list:
            tmp.append(token)
            word = self.__get_word_from_token(token)
            if reg.pnwn.search(word):
                parts.append(tmp)
                tmp = []
        return parts

    def __get_word_from_token(self, token: str or Tuple[str, str]) -> str:
        if type(token) == str:
            return token
        else:
            tup = tuple(token)
            return tup[0]

    def __join_tokens(self, token_list: List[str or Tuple[str, str]]) -> str:
        result = []
        for token in token_list:
            word = self.__get_word_from_token(token)
            result.append(word)
        return "".join(result)

    def make_samples(
        self,
        text: str,
        tokenizer: Optional[
            Callable[[str], List[str or Tuple[str, str]]]] = None
    ) -> Dict[str, str]:
        """
        Make negative samples.

        Parameters
        -----------
        text: The given text. Usually a sentence.
        tokenizer: Input a text, output a List of tokens. A token is a word or a (word, flag) tuple.

        Returns
        --------
        output: A dict of different kinds of negative samples.
        """
        if self.len_types == 0:
            return {}
        if not tokenizer:
            if reg.pchi.search(text):
                tokenizer = cut_zhchar
            else:
                def tokenizer(x): return x.split()
        tokens = tokenizer(text)
        if len(tokens) == 0:
            return {}
        result = {}
        indep_samples = self.independent_sampling(tokens)
        dep_sample = self.dependent_sampling(tokens)
        if indep_samples:
            for i, typ in enumerate(self.types):
                new_tokens = indep_samples[i]
                result[typ] = self.__join_tokens(new_tokens)
            result["together"] = self.__join_tokens(dep_sample)
        return result


@dataclass
class SentenceLevelSampler(Sampler):

    """
    Random choose an index. 
    - Insert a copy.
    - Delete.
    - Swap with the prev or the next one.

    We only deal with ONE sentence once.
    So you'd better use a paragraph as input.

    Parameters
    -----------
    types: Sampling methods. You should take care of the order.
    """

    types: List[str] = field(
        default_factory=lambda: ["delete", "swap", "insert"])

    def __post_init__(self):
        self.check_types()

    def independent_sampling(self, text_list: List[str]) -> List[List[str]]:
        result = []
        text_list = copy.deepcopy(text_list)
        length = len(text_list)
        for i, typ in enumerate(self.types):
            idx = np.random.choice(length, 1).tolist()[0]
            if typ == "insert":
                new = text_list[:idx] + [text_list[idx]] + text_list[idx:]
            elif typ == "delete":
                new = [s for (i, s) in enumerate(text_list) if i != idx]
            else:
                new = swap(text_list, idx, 0, length-1)
            result.append(new)
        return result

    def dependent_sampling(self, text_list: List[str]) -> List[str]:
        text_list = copy.deepcopy(text_list)
        for i, typ in enumerate(self.types):
            # 每次重新更新长度
            length = len(text_list)
            if length == 0:
                continue
            idx = np.random.choice(length, 1).tolist()[0]
            if typ == "insert":
                text_list = text_list[:idx] + \
                    [text_list[idx]] + text_list[idx:]
            elif typ == "delete":
                text_list = [s for (i, s) in enumerate(text_list) if i != idx]
            else:
                text_list = swap(text_list, idx, 0, length-1)
        return text_list

    def make_samples(self, text: str, level: str = "sent") -> List[str]:
        """
        Parameters
        -------------
        text: The given text. Always a paragraph.
        level: The sampling level. Could be one of {"sent", "subsent"}.

        Returns
        --------
        output: A dict of different kinds of negative samples.
        """
        if level == "sent":
            text_list = cut_part(text, psent)
        else:
            text_list = cut_part(text, psubsent)
        if len(text_list) == 0:
            return {}
        result = {}
        indep_samples = self.independent_sampling(text_list)
        dep_sample = self.dependent_sampling(text_list)
        if indep_samples:
            for i, typ in enumerate(self.types):
                new = indep_samples[i]
                result[typ] = "".join(new)
            result["together"] = "".join(dep_sample)
        return result
