from pnlp.utils import pstr, strip_text


def test_pstr1():
    s1 = pstr("123")
    s2 = "1"
    assert s1 - s2 == "23"


def test_pstr2():
    s1 = pstr("123")
    s2 = "123"
    assert s1 - s2 == ""


def test_pstr3():
    s1 = pstr("123")
    s2 = "234"
    assert s1 - s2 == "1"


def test_pstr4():
    s1 = pstr("123")
    s2 = "456"
    assert s1 - s2 == "123"


def test_pstr5():
    s1 = pstr("")
    s2 = "456"
    assert s1 - s2 == ""


def test_strip_text_work():
    assert strip_text(" 1", "left") == "1"
    assert strip_text("1 ", "right") == "1"
    assert strip_text(" 1 ", "both") == "1"
    assert strip_text("1", None) == "1"


def test_strip_text_not():
    assert strip_text(" 1", "right") == " 1"
    assert strip_text("1 ", "left") == "1 "
    assert strip_text(" 1 ", "other") == " 1 "
    assert strip_text(" 1 ", None) == " 1 "
