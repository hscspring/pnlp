import pytest

from pnlp.pnorm import NumNorm

c2a = NumNorm()


def test_chinese2arabic1():
    s = "一亿三千万"
    assert c2a.zh2num(s) == 130000000


def test_chinese2arabic2():
    s = "一万五千六百三十八"
    assert c2a.zh2num(s) == 15638


def test_chinese2arabic3():
    s = "壹仟两百"
    assert c2a.zh2num(s) == 1200


def test_chinese2arabic4():
    s = "壹仟两百零三"
    assert c2a.zh2num(s) == 1203


def test_chinese2arabic5():
    s = "壹仟两百一十五"
    assert c2a.zh2num(s) == 1215


def test_chinese2arabic6():
    s = "壹仟两百九十"
    assert c2a.zh2num(s) == 1290


def test_chinese2arabic7():
    s = "十一"
    assert c2a.zh2num(s) == 11


def test_chinese2arabic8():
    s = "八十八"
    assert c2a.zh2num(s) == 88


def test_chinese2arabic9():
    s = "三"
    assert c2a.zh2num(s) == 3


def test_chinese2arabic10():
    s = "两百五十"
    assert c2a.zh2num(s) == 250


def test_chinese2arabic11():
    s = "两百"
    assert c2a.zh2num(s) == 200


def test_chinese2arabic12():
    s = "两百零五"
    assert c2a.zh2num(s) == 205


def test_chinese2arabic13():
    s = "两百二十五"
    assert c2a.zh2num(s) == 225


def test_chinese2arabic14():
    s = "二十万五千"
    assert c2a.zh2num(s) == 205000


def test_chinese2arabic15():
    s = "两百三十九万四千八百二十三"
    assert c2a.zh2num(s) == 2394823


def test_chinese2arabic16():
    s = "一千三百万"
    assert c2a.zh2num(s) == 13000000


def test_chinese2arabic17():
    s = "万"
    assert c2a.zh2num(s) == "万"


def test_chinese2arabic18():
    s = "亿"
    assert c2a.zh2num(s) == "亿"


def test_chinese2arabic19():
    s = "千"
    assert c2a.zh2num(s) == "千"


def test_chinese2arabic20():
    s = "百"
    assert c2a.zh2num(s) == "百"


def test_chinese2arabic21():
    s = "零"
    assert c2a.zh2num(s) == 0


def test_arabic2chinese1():
    num = 0
    assert c2a.num2zh(num) == "零"


def test_arabic2chinese2():
    num = 1
    assert c2a.num2zh(num) == "一"


def test_arabic2chinese3():
    num = 10
    assert c2a.num2zh(num) == "一十"


def test_arabic2chinese4():
    num = 12
    assert c2a.num2zh(num) == "一十二"


def test_arabic2chinese5():
    num = 22
    assert c2a.num2zh(num) == "二十二"


def test_arabic2chinese6():
    num = 100
    assert c2a.num2zh(num) == "一百"


def test_arabic2chinese7():
    num = 101
    assert c2a.num2zh(num) == "一百零一"


def test_arabic2chinese8():
    num = 110
    assert c2a.num2zh(num) == "一百一十"


def test_arabic2chinese9():
    num = 112
    assert c2a.num2zh(num) == "一百一十二"


def test_arabic2chinese10():
    num = 1000
    assert c2a.num2zh(num) == "一千"


def test_arabic2chinese11():
    num = 1001
    assert c2a.num2zh(num) == "一千零一"


def test_arabic2chinese12():
    num = 1011
    assert c2a.num2zh(num) == "一千零一十一"


def test_arabic2chinese13():
    num = 1101
    assert c2a.num2zh(num) == "一千一百零一"


def test_arabic2chinese14():
    num = 1010
    assert c2a.num2zh(num) == "一千零一十"


def test_arabic2chinese15():
    num = 1100
    assert c2a.num2zh(num) == "一千一百"


def test_arabic2chinese16():
    num = 1110
    assert c2a.num2zh(num) == "一千一百一十"


def test_arabic2chinese17():
    num = 1111
    assert c2a.num2zh(num) == "一千一百一十一"


def test_arabic2chinese18():
    num = 100000
    assert c2a.num2zh(num) == "一十万"


def test_arabic2chinese19():
    num = 110000
    assert c2a.num2zh(num) == "一十一万"


def test_arabic2chinese20():
    num = 1000000
    assert c2a.num2zh(num) == "一百万"


def test_arabic2chinese21():
    num = 1010000
    assert c2a.num2zh(num) == "一百零一万"


def test_arabic2chinese22():
    num = 1100000
    assert c2a.num2zh(num) == "一百一十万"


def test_arabic2chinese23():
    num = 1110000
    assert c2a.num2zh(num) == "一百一十一万"


def test_arabic2chinese24():
    num = 100000000
    assert c2a.num2zh(num) == "一亿"


def test_arabic2chinese25():
    num = 110000000
    assert c2a.num2zh(num) == "一亿一千万"


def test_arabic2chinese26():
    num = 111000000
    assert c2a.num2zh(num) == "一亿一千一百万"


def test_arabic2chinese27():
    num = 101000000
    assert c2a.num2zh(num) == "一亿零一百万"


def test_arabic2chinese28():
    num = 1000000000000
    assert c2a.num2zh(num) == "一万亿"


def test_arabic2chinese29():
    num = 1100000000000
    assert c2a.num2zh(num) == "一万一千亿"


def test_arabic2chinese30():
    # 一兆一亿
    num = 11000000000000
    assert c2a.num2zh(num) == "超大"


def test_arabic2chinese31():
    num = 1110011
    assert c2a.num2zh(num) == "一百一十一万零一十一"


def test_arabic2chinese_money2():
    num = 112
    assert c2a.num2zh(num).to_money() == "壹佰壹拾贰"


def test_arabic2chinese_money2():
    num = 1111
    assert c2a.num2zh(num).to_money() == "壹仟壹佰壹拾壹"


def test_arabic2chinese_money3():
    num = 1010000
    assert c2a.num2zh(num).to_money() == "壹佰零壹萬"

