import os
import re
import sys
import pytest
import types

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

from ptxt import Text, Regex, cut_sentence
reg = Regex()


@pytest.fixture(params=reg.patnames)
def get_regex(request):
    return reg.patdict[request.param]

def test_regex_well(get_regex):
    assert isinstance(get_regex, re.Pattern)


@pytest.fixture(params=reg.patnames)
def get_patten(request):
    return [request.param]

def test_Text_extract(get_patten):
    text = "这是，测试fdsf234*(&( 返回类型的文本。"
    res = Text(text, get_patten).extract
    assert isinstance(res, dict) == True
    assert isinstance(res.mats, list) == True
    assert isinstance(res.locs, list) == True

def test_Text_clean(get_patten):
    text = "这是，测试fdsf234*(&( 返回类型的文本。"
    res = Text(text, get_patten).clean
    assert isinstance(res, str) == True


def test_pattern_string_invalid():
    try:
        pt = Text("", ["XX"])
    except Exception as e:
        assert "built-in" in str(e)


def test_pattern_invalid():
    try:
        pt = Text("", [lambda x: x])
    except Exception as e:
        assert "RE" in str(e)


@pytest.fixture
def text_chi():
    text = "你好。jefj*(&-1)这是中文测试！"
    return text


def test_Text_extract_chi(text_chi):
    res = Text(text_chi, ['chi']).extract
    assert "".join(res.mats) == "你好这是中文测试"

def test_Text_clean_chi(text_chi):
    res = Text(text_chi, ['chi']).clean
    assert res == "。jefj*(&-1)！"


@pytest.fixture
def text_pun():
    text = "你好，这是标点,.!;<>()符号测试。"
    return text

def test_Text_extract_pun(text_pun):
    res = Text(text_pun, ['nwn']).extract
    assert "".join(res.mats) == "，,.!;<>()。"

def test_Text_clean_pun(text_pun):
    res = Text(text_pun, ['nwn']).clean
    assert res == "你好这是标点符号测试"


@pytest.fixture
def text_whi():
    text = "你好，这是空白 \t\n符号测试。"
    return text

def test_Text_extract_whi(text_whi):
    res = Text(text_whi, ['whi']).extract
    assert "".join(res.mats) == " \t\n"

def test_Text_clean_whi(text_whi):
    res = Text(text_whi, ['whi']).clean
    assert res == "你好，这是空白符号测试。"


@pytest.fixture
def text_nwh():
    text = "你好，这是非空白 \t\n符号测试。"
    return text

def test_Text_extract_nwh(text_nwh):
    res = Text(text_nwh, ['nwh']).extract
    assert "".join(res.mats) == "你好，这是非空白符号测试。"

def test_Text_clean_nwh(text_nwh):
    res = Text(text_nwh, ['nwh']).clean
    assert res == " \t\n"


@pytest.fixture
def text_wnb():
    text = "你好，这是词与word数字number测试。"
    return text

def test_Text_extract_wnb(text_wnb):
    res = Text(text_wnb, ['wnb']).extract
    assert "".join(res.mats) == "你好这是词与word数字number测试"

def test_Text_clean_wnb(text_wnb):
    res = Text(text_wnb, ['wnb']).clean
    assert res == "，。"


@pytest.fixture
def text_nwn():
    text = "你好，这是非词或word数字number测试。"
    return text

def test_Text_extract_nwn(text_nwn):
    res = Text(text_nwn, ['nwn']).extract
    assert "".join(res.mats) == "，。"

def test_Text_clean_nwn(text_nwn):
    res = Text(text_nwn, ['nwn']).clean
    assert res == "你好这是非词或word数字number测试"


@pytest.fixture
def text_eng():
    text = "你好，这#￥是英文English测试。"
    return text

def test_Text_extract_eng(text_eng):
    res = Text(text_eng, ['eng']).extract
    assert "".join(res.mats) == "English"

def test_Text_clean_eng(text_eng):
    res = Text(text_eng, ['eng']).clean
    assert res == "你好，这#￥是英文测试。"


@pytest.fixture
def text_num():
    text = "你好，这#￥是数字2, +2, -2, 2.1, -2.2, 1/5, 2:3, -2/5, 2%, 2.5%测试。"
    return text

def test_Text_extract_num(text_num):
    res = Text(text_num, ['num']).extract
    assert "".join(res.mats) == "2+2-22.1-2.21/52:3-2/52%2.5%"

def test_Text_clean_num(text_num):
    res = Text(text_num, ['num']).clean
    assert res == "你好，这#￥是数字, , , , , , , , , 测试。"


@pytest.fixture
def text_pic():
    text = "你好，这#￥是![p1](https://xxx.jpeg)图片![](yyy.png)测试https://z.jpg。"
    return text

def test_Text_extract_pic(text_pic):
    res = Text(text_pic, ['pic']).extract
    assert "".join(res.mats) == "![p1](https://xxx.jpeg)![](yyy.png)https://z.jpg"

def test_Text_clean_pic(text_pic):
    res = Text(text_pic, ['pic']).clean
    assert res == "你好，这#￥是图片测试。"


@pytest.fixture
def text_lnk():
    text = "你好，这#￥是链接[link](https://yam.gift)测试http://yam.gift。"
    return text

def test_Text_extract_lnk(text_lnk):
    res = Text(text_lnk, ['lnk']).extract
    assert "".join(res.mats) == "[link](https://yam.gift)http://yam.gift"

def test_Text_clean_lnk(text_lnk):
    res = Text(text_lnk, ['lnk']).clean
    assert res == "你好，这#￥是链接测试。"


@pytest.fixture
def text_emj():
    text = "你好，这#￥是表情😁测试😜🌹。"
    return text

def test_Text_extract_emj(text_emj):
    res = Text(text_emj, ['emj']).extract
    assert "".join(res.mats) == "😁😜🌹"

def test_Text_clean_emj(text_emj):
    res = Text(text_emj, ['emj']).clean
    assert res == "你好，这#￥是表情测试。"


@pytest.fixture
def text_len():
    text = "这是https://www.yam.gift长度测试，《 》*)FSJfdsjf😁![](http://xx.jpg)。233."
    return text


def test_Text_len_all(text_len):
    res = Text(text_len).len_all
    assert res == 64

def test_Text_len_nwh(text_len):
    res = Text(text_len).len_nwh
    assert res == 63

def test_Text_len_chi(text_len):
    res = Text(text_len).len_chi
    assert res == 6

def test_Text_len_wnb(text_len):
    res = Text(text_len).len_wnb
    assert res == 41

def test_Text_len_pun(text_len):
    res = Text(text_len).len_pun
    assert res == 14

def test_Text_len_eng(text_len):
    res = Text(text_len).len_eng
    assert res == 32

def test_Text_len_num(text_len):
    res = Text(text_len).len_num
    assert res == 3


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



if __name__ == '__main__':
    print(reg.patnames)
