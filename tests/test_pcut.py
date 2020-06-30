import re
import pytest

from pnlp.pcut import cut_sentence, cut_zhchar


def test_text2char1():
    text = "我喜欢你。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "。"]


def test_text2char2():
    text = "我 喜欢 你。"
    ret = cut_zhchar(text)
    assert ret == ["我", " ", "喜", "欢", " ", "你", "。"]


def test_text2char3():
    text = "我喜欢like你。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "like", "你", "。"]


def test_text2char4():
    text = "我喜欢你233。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "233", "。"]


def test_text2char5():
    text = "我喜欢你3.14。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "3.14", "。"]


def test_text2char6():
    text = "我喜欢你100%。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "100%", "。"]


def test_text2char7():
    text = "我喜欢你2/3。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "2/3", "。"]


def test_text2char8():
    text = "我喜欢你-2。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "-2", "。"]


def test_text2char9():
    text = "我喜欢你2、3。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "2", "、", "3", "。"]


def test_text2char10():
    text = "我喜欢你。。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "。", "。"]


def test_text2char11():
    text = "我喜欢你A-B。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "A-B", "。"]


def test_text2char12():
    text = "我喜欢你A_B。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "A", "_", "B", "。"]


def test_text2char13():
    text = "我喜欢你C++。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "C", "+", "+", "。"]


def test_text2char14():
    text = "我喜欢你R&B。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "R", "&", "B", "。"]


def test_text2char15():
    text = "#我喜欢你。"
    ret = cut_zhchar(text)
    assert ret == ["#", "我", "喜", "欢", "你", "。"]


def test_text2char16():
    text = "我 喜欢 你。"
    ret = cut_zhchar(text, remove_blank=True)
    assert ret == ["我", "喜", "欢", "你", "。"]


def test_text2sent1():
    text = "我喜欢你，你呢？哈哈，我不告诉你。"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，你呢？"
    assert ret[1] == "哈哈，我不告诉你。"


def test_text2sent2():
    text = "我喜欢你，你呢！哈哈，我不告诉你"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，你呢！"
    assert ret[1] == "哈哈，我不告诉你"


def test_text2sent3():
    text = "我喜欢你，「哈哈」。我不告诉你~~~"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，「哈哈」。"
    assert ret[1] == "我不告诉你~~~"


def test_text2sent4():
    text = "我喜欢你，“哈哈”.我不告诉你……"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，“哈哈”."
    assert ret[1] == "我不告诉你……"


def test_text2sent5():
    text = "我喜欢你，“哈哈” 我不告诉你；"
    ret = cut_sentence(text)
    assert len(ret) == 1
    assert ret[0] == "我喜欢你，“哈哈” 我不告诉你；"


def test_text2sent6():
    text = "我喜欢你，“哈哈。” 我不告诉你!"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，“哈哈。”"
    assert ret[1] == " 我不告诉你!"


def test_text2sent7():
    text = "我喜欢你(haha). 我不告诉你～"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你(haha)."
    assert ret[1] == " 我不告诉你～"


def test_text2sent8():
    text = "我喜欢你, “哈哈……”。“我不告诉你.”"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你, “哈哈……”。"
    assert ret[1] == "“我不告诉你.”"


def test_text2sent9():
    text = "我喜欢你&“哈哈？”“我不告诉你”"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你&“哈哈？”"
    assert ret[1] == "“我不告诉你”"


def test_text2sent10():
    text = "我喜欢你，"
    ret = cut_sentence(text)
    assert len(ret) == 1
    assert ret[0] == "我喜欢你，"


def test_text2sent11():
    text = "我喜欢你"
    ret = cut_sentence(text)
    assert len(ret) == 1
    assert ret[0] == "我喜欢你"


def test_text2sent12():
    text = "我喜欢\n你"
    ret = cut_sentence(text)
    assert len(ret) == 1
    assert ret[0] == "我喜欢\n你"
