import pytest
from pnlp.penh import swap, SentenceLevelSampler, TokenLevelSampler
from pnlp.pcut import psubsent, cut_part, cut_zhchar


def test_swap_middle():
    lst = [1, 2, 3, 4, 5]
    new = swap(lst, 2, 0, 4)
    assert new == [1, 3, 2, 4, 5] or new == [1, 2, 4, 3, 5]


def test_swap_start():
    lst = [1, 2, 3]
    new = swap(lst, 0, 0, 2)
    assert new == [2, 1, 3]


def test_swap_end():
    lst = [1, 2, 3]
    new = swap(lst, 2, 0, 2)
    assert new == [1, 3, 2]


def cut_words(text: str) -> list:
    return [
        '人', '为什么', '活着', '？',
        '生而为', '人', '必须', '要', '有', '梦想', '！',
        '还要', '有', '尽可能', '多', '的', '精神', '体验', '。']


def cut_wps(text: str) -> list:
    return [
        ('人', 'n'), ('为什么', 'r'), ('活着', 'v'), ('？', 'w'),
        ('生而为人', 'v'), ('必须', 'd'), ('要', 'v'),
        ('有', 'v'), ('梦想', 'n'), ('！', 'w'),
        ('还要', 'v'), ('有', 'v'), ('尽可能', 'd'), ('多', 'a'),
        ('的', 'u'), ('精神', 'n'), ('体验', 'vn'), ('。', 'w')
    ]


def test_token_level_sampler():
    tls = TokenLevelSampler()
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    res = tls.make_samples(text)
    assert type(res) == dict
    assert len(res) == 4


def test_token_level_sampler_none():
    tls = TokenLevelSampler(types=[])
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    res = tls.make_samples(text)
    assert res == {}


def test_token_level_sampler_none_text():
    tls = TokenLevelSampler()
    text = ""
    res = tls.make_samples(text)
    assert res == {}


def test_token_level_sampler_single_sent():
    tls = TokenLevelSampler()
    text = "人为什么活着？"
    res = tls.make_samples(text)
    assert len(res) == 4


def test_token_level_sampler_independent_sampling():
    tls = TokenLevelSampler()
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    tokens = cut_zhchar(text)
    res = tls.independent_sampling(tokens)
    assert type(res) == list
    assert len(res) == 3


def test_token_level_sampler_dependent_sampling():
    tls = TokenLevelSampler()
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    tokens = cut_zhchar(text)
    res = tls.dependent_sampling(tokens)
    assert type(res) == list
    assert type(res[0]) == str


def test_token_level_sampler_delete():
    tls = TokenLevelSampler(types=["delete"])
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    res = tls.make_samples(text)
    assert type(res) == dict
    assert len(res) == 2


def test_token_level_sampler_swap():
    tls = TokenLevelSampler(types=["swap"])
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    res = tls.make_samples(text)
    assert type(res) == dict
    assert len(res) == 2


def test_token_level_sampler_insert():
    tls = TokenLevelSampler(types=["insert"])
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    res = tls.make_samples(text)
    assert type(res) == dict
    assert len(res) == 2


def test_token_level_sampler_token_spliter():
    tls = TokenLevelSampler()
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    res = tls.make_samples(text, cut_words)
    assert len(res) == 4


def test_token_level_sampler_token_pos_spliter():
    tls = TokenLevelSampler()
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    res = tls.make_samples(text, cut_wps)
    assert len(res) == 4


def test_token_level_sampler_delete_sampling():
    tls = TokenLevelSampler()
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    tokens = cut_words(text)
    res = tls.delete_sampling(tokens, [2])
    assert type(res) == list
    assert len(res) + 1 == len(tokens)


def test_token_level_sampler_insert_sampling():
    tls = TokenLevelSampler()
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    tokens = cut_words(text)
    res = tls.insert_sampling(tokens, [2, 6])
    assert type(res) == list
    assert len(res) - 2 == len(tokens)


def test_token_level_sampler_swap_sampling():
    tls = TokenLevelSampler()
    text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
    tokens = cut_words(text)
    res = tls.swap_sampling(tokens, [5, 8])
    assert type(res) == list
    assert len(res) == len(tokens)


def test_sentence_level_sampler():
    sls = SentenceLevelSampler()
    text = "我爱你。你爱我。"
    res = sls.make_samples(text)
    assert type(res) == dict
    assert len(res) == 4


def test_sentence_level_sampler_none():
    sls = SentenceLevelSampler([])
    text = "我爱你。你爱我。"
    assert sls.make_samples(text) == {}


def test_sentence_level_sampler_single_sent():
    sls = SentenceLevelSampler()
    text = "我爱你。"
    assert len(sls.make_samples(text)) == 4


def test_sentence_level_sampler_none_text():
    sls = SentenceLevelSampler()
    text = ""
    assert sls.make_samples(text) == {}


def test_sentence_level_sampler_independent_sampling():
    sls = SentenceLevelSampler()
    text = "写代码。写好代码。"
    text_list = cut_part(text, psubsent)
    res = sls.independent_sampling(text_list)
    assert type(res) == list
    assert len(res) == 3
    assert len(res[0]) == 1
    assert len(res[1]) == 2
    assert len(res[2]) == 3


def test_sentence_level_sampler_dependent_sampling():
    sls = SentenceLevelSampler()
    text = "写代码。多写代码。写好代码。"
    text_list = cut_part(text, psubsent)
    res = sls.dependent_sampling(text_list)
    assert type(res) == list
    assert len(res) == 3


def test_sentence_level_sampler_insert():
    sls = SentenceLevelSampler(types=["insert"])
    text = "我爱你。你爱我。NLP 很有意思。简洁最重要。"
    res = sls.make_samples(text)
    assert len(res) == 2


def test_sentence_level_sampler_delete():
    sls = SentenceLevelSampler(types=["delete"])
    text = "我爱你。你爱我。NLP 很有意思。简洁最重要。"
    res = sls.make_samples(text)
    assert len(res) == 2


def test_sentence_level_sampler_swap():
    sls = SentenceLevelSampler(types=["swap"])
    text = "我爱你。你爱我。NLP 很有意思。简洁最重要。"
    res = sls.make_samples(text)
    assert len(res) == 2
