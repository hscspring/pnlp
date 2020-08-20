import re
import pytest

from pnlp.ptxt import Text, Regex, Length
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
    res = Text(get_patten).extract(text)
    assert isinstance(res, dict) == True
    assert isinstance(res.mats, list) == True
    assert isinstance(res.locs, list) == True


def test_Text_clean(get_patten):
    text = "这是，测试fdsf234*(&( 返回类型的文本。"
    res = Text(get_patten).clean(text)
    assert isinstance(res, str) == True


def test_pattern_string_invalid():
    try:
        pt = Text(["XX"])
    except Exception as e:
        assert "built-in" in str(e)


def test_pattern_invalid():
    try:
        pt = Text([lambda x: x])
    except Exception as e:
        assert "RE" in str(e)


@pytest.fixture
def text_chi():
    text = "你好。jefj*(&-1)这是中文测试！"
    return text


def test_Text_extract_chi(text_chi):
    res = Text(['chi']).extract(text_chi)
    assert "".join(res.mats) == "你好这是中文测试"
    assert res.text == "你好这是中文测试"


def test_Text_clean_chi(text_chi):
    res = Text(['chi']).clean(text_chi)
    assert res == "。jefj*(&-1)！"


@pytest.fixture
def text_pun():
    text = "你好，这是标点,.!;<>()符号测试。"
    return text


def test_Text_extract_pun(text_pun):
    res = Text(['nwn']).extract(text_pun)
    assert "".join(res.mats) == "，,.!;<>()。"
    assert res.text == "，,.!;<>()。"


def test_Text_clean_pun(text_pun):
    res = Text(['nwn']).clean(text_pun)
    assert res == "你好这是标点符号测试"


@pytest.fixture
def text_whi():
    text = "你好，这是空白 \t\n符号测试。"
    return text


def test_Text_extract_whi(text_whi):
    res = Text(['whi']).extract(text_whi)
    assert "".join(res.mats) == " \t\n"
    assert res.text == " \t\n"


def test_Text_clean_whi(text_whi):
    res = Text(['whi']).clean(text_whi)
    assert res == "你好，这是空白符号测试。"


@pytest.fixture
def text_nwh():
    text = "你好，这是非空白 \t\n符号测试。"
    return text


def test_Text_extract_nwh(text_nwh):
    res = Text(['nwh']).extract(text_nwh)
    assert "".join(res.mats) == "你好，这是非空白符号测试。"
    assert res.text == "你好，这是非空白符号测试。"


def test_Text_clean_nwh(text_nwh):
    res = Text(['nwh']).clean(text_nwh)
    assert res == " \t\n"


@pytest.fixture
def text_wnb():
    text = "你好，这是词与word数字number测试。"
    return text


def test_Text_extract_wnb(text_wnb):
    res = Text(['wnb']).extract(text_wnb)
    assert "".join(res.mats) == "你好这是词与word数字number测试"
    assert res.text == "你好这是词与word数字number测试"


def test_Text_clean_wnb(text_wnb):
    res = Text(['wnb']).clean(text_wnb)
    assert res == "，。"


@pytest.fixture
def text_nwn():
    text = "你好，这是非词或word数字number测试。"
    return text


def test_Text_extract_nwn(text_nwn):
    res = Text(['nwn']).extract(text_nwn)
    assert "".join(res.mats) == "，。"
    assert res.text == "，。"


def test_Text_clean_nwn(text_nwn):
    res = Text(['nwn']).clean(text_nwn)
    assert res == "你好这是非词或word数字number测试"


@pytest.fixture
def text_eng():
    text = "你好，这#￥是英文English测试。"
    return text


def test_Text_extract_eng(text_eng):
    res = Text(['eng']).extract(text_eng)
    assert "".join(res.mats) == "English"
    assert res.text == "English"


def test_Text_clean_eng(text_eng):
    res = Text(['eng']).clean(text_eng)
    assert res == "你好，这#￥是英文测试。"


@pytest.fixture
def text_num():
    text = "你好，这#￥是数字2, +2, -2, 2.1, -2.2, 1/5, 2:3, -2/5, 2%, 2.5%测试。"
    return text


def test_Text_extract_num(text_num):
    res = Text(['num']).extract(text_num)
    assert "".join(res.mats) == "2+2-22.1-2.21/52:3-2/52%2.5%"
    assert res.text == "2+2-22.1-2.21/52:3-2/52%2.5%"


def test_Text_clean_num(text_num):
    res = Text(['num']).clean(text_num)
    assert res == "你好，这#￥是数字, , , , , , , , , 测试。"


@pytest.fixture
def text_pic():
    text = "你好，这#￥是![p1](https://xxx.jpeg)图片![](yyy.png)测试https://z.jpg。"
    return text


def test_Text_extract_pic(text_pic):
    res = Text(['pic']).extract(text_pic)
    assert "".join(
        res.mats) == "![p1](https://xxx.jpeg)![](yyy.png)https://z.jpg"
    assert res.text == "![p1](https://xxx.jpeg)![](yyy.png)https://z.jpg"


def test_Text_clean_pic(text_pic):
    res = Text(['pic']).clean(text_pic)
    assert res == "你好，这#￥是图片测试。"


@pytest.fixture
def text_lnk():
    text = "你好，www.g.com，这#￥是链接[link](https://yam.gift)测试http://yam.gift。"
    return text


def test_Text_extract_lnk(text_lnk):
    res = Text(['lnk']).extract(text_lnk)
    assert "".join(res.mats) == "www.g.com[link](https://yam.gift)http://yam.gift"
    assert res.text == "www.g.com[link](https://yam.gift)http://yam.gift"


def test_Text_clean_lnk(text_lnk):
    res = Text(['lnk']).clean(text_lnk)
    assert res == "你好，，这#￥是链接测试。"


@pytest.fixture
def text_emj():
    text = "你好，这#￥是表情😁测试😜🌹。"
    return text


def test_Text_extract_emj(text_emj):
    res = Text(['emj']).extract(text_emj)
    assert "".join(res.mats) == "😁😜🌹"
    assert res.text == "😁😜🌹"


def test_Text_clean_emj(text_emj):
    res = Text(['emj']).clean(text_emj)
    assert res == "你好，这#￥是表情测试。"


@pytest.fixture
def text_len():
    text = "这是https://www.yam.gift长度测试，《 》*)FSJfdsjf😁![](http://xx.jpg)。233."
    return text


def test_Text_len_all(text_len):
    res = Length(text_len).len_all
    assert res == 64


def test_Text_len_nwh(text_len):
    res = Length(text_len).len_nwh
    assert res == 63


def test_Text_len_chi(text_len):
    res = Length(text_len).len_chi
    assert res == 6


def test_Text_len_wnb(text_len):
    res = Length(text_len).len_wnb
    assert res == 41


def test_Text_len_pun(text_len):
    res = Length(text_len).len_pun
    assert res == 14


def test_Text_len_eng(text_len):
    res = Length(text_len).len_eng
    assert res == 32


def test_Text_len_num(text_len):
    res = Length(text_len).len_num
    assert res == 3


if __name__ == '__main__':
    print(reg.patnames)
