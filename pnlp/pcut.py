import itertools
import re
from .ptxt import Regex
from .utils import pstr


psent = re.compile(r'''
    \n+
    |
    [。.！!?？…]+[”][。.!！?？…～~]?
    |
    (?<=[ \u3000a-zA-Z"”》）)〉〕】>」』\u4e00-\u9fa5])[。.!！?？…～~]+
    ''', re.UNICODE | re.VERBOSE)
psubsent = re.compile(r'''
    \n+
    |
    [。.！!?？…]+[”][。.!！?？…～~]?
    |
    (?<=[ \u3000a-zA-Z"”》）)〉〕】>」』\u4e00-\u9fa5])[,，、:：；;。.!！?？…～~]+
    ''', re.UNICODE | re.VERBOSE)
# referenced from jieba
punzh = pstr(Regex.pun_zh) - "-"  # for minus number eg -2
punen = pstr(Regex.pun_en) - "."  # for float number eg 1.3
pun = punzh + punen
pzh = re.compile(rf"([\u4E00-\u9FD5{pun}+#&])", re.UNICODE)
pen = re.compile(r"([a-zA-Z]+)", re.UNICODE)
pskip = re.compile(r"(\s)", re.UNICODE)
pspecial = re.compile(r"([-.])")  # split to single
pnum = re.compile(r"""
    ([-]?\d{1,}[.]?\d{0,}%)
    |
    ([-]?\d{1,}[./]?\d{0,})    
    """, re.UNICODE | re.VERBOSE)


def cut_zhchar(text: str, remove_blank: bool = False) -> list:
    lst = []
    blocks = pzh.split(text)
    for block in blocks:
        if not block:
            continue
        if pzh.match(block):
            for char in block:
                lst.append(char)
        else:
            skips = pskip.split(block)
            for skip in skips:
                if pen.search(skip):
                    for en_part in pen.split(skip):
                        if en_part:
                            spe = pspecial.search(en_part)
                            if not spe:
                                lst.append(en_part)
                            else:
                                for spe_part in pspecial.split(en_part):
                                    if spe_part:
                                        lst.append(spe_part)
                elif pnum.search(skip):
                    if skip[-1] != ".":
                        lst.append(skip)
                    else:
                        i = 0
                        while skip[-1] == ".":
                            i += 1
                            skip = skip[:-1]
                        lst.append(skip)
                        for _ in range(i):
                            lst.append(".")
                else:
                    if remove_blank:
                        skip = pskip.sub("", skip)
                    if skip:
                        lst.append(skip)
    return lst


def cut_part(
        text: str,
        split_pattern: re.Pattern,
        with_spliter: bool = True,
        with_offset: bool = False) -> list:
    """
    Cut text to parts by the given Regex Pattern.

    Parameters
    ----------
    text: raw text.
    split_pattern: how to split text.
    with_spliter: whether the parts contain spliters.
    with_offset: whether the parts contain offsets.

    Returns
    --------
    out: cutted parts.
    """
    spliters = split_pattern.findall(text)
    length = len(spliters)
    lst = []
    start = 0
    for i, part in enumerate(split_pattern.split(text)):
        if i < length:
            if with_spliter:
                part = part + spliters[i]
                len_spliter = 0
            else:
                len_spliter = len(spliters[i])
        else:
            len_spliter = 0
        end = start + len(part) + len_spliter
        if part:
            if with_offset:
                item = (part, start, end)
            else:
                item = part
            lst.append(item)
        start = end
    return lst


def cut_sentence(text: str) -> list:
    return cut_part(text, psent, True, False)


def combine_bucket(
        parts: list,
        threshold: int,
        truncate: bool = False,
        keep_remain: bool = False) -> list:
    """
    Convert parts to buckets with given length(threshold).

    Parameters
    ----------
    parts: the given parts.
    threshold: bucket length.
    truncate: whether to truncate those whose length is bigger than threshold.
    keep_remain: when truncate=True, whether to keep the remain parts.

    Returns
    out: list of bucket.
    -------
    """
    def deal_long_part(part: str) -> list:
        result = []
        if truncate:
            if keep_remain:
                len_subparts = len(part) // threshold + 1
                for i in range(len_subparts):
                    sub_part = part[i*threshold: (i+1)*threshold]
                    if sub_part:
                        result.append(sub_part)
            else:
                result.append(part[:threshold])
        else:
            result.append(part)
        return result

    buckets = []
    while parts:
        part = parts.pop(0)
        # directly add to buckets when a part is longer than threshold
        if len(part) > threshold:
            sub_parts = deal_long_part(part)
            buckets.append(sub_parts)
        else:
            while parts and len(part) < threshold:
                another = parts[0]
                if len(part + another) > threshold:
                    break
                else:
                    part += parts.pop(0)
            buckets.append([part])
    result = list(itertools.chain(*buckets))
    return result



