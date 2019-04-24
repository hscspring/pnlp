import os
import re
import sys
import pytest
import types

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)


from ptxt import Text, Regex

reg = Regex()

@pytest.fixture(params=reg.patnames)
def get_regex(request):
    return reg.patdict[request.param]

def test_regex_well(get_regex):
    assert isinstance(get_regex, re.Pattern)

@pytest.fixture
def get_text():
    text = "你好。jefj*(&-1)这是测试！"
    return text

def test_Text_extract_chi(get_text):
    res = Text(get_text, 'chi').extract
    assert isinstance(res, dict) == True
    assert isinstance(res.mats, list) == True
    assert "".join(res.mats) == "你好这是测试"

def test_Text_clean_chi(get_text):
    res = Text(get_text, 'chi').clean
    assert res == "。jefj*(&-1)！"

def test_Text_clean(get_text):
    res = Text(get_text, 'nwn').clean
    assert res == "你好jefj1这是测试"

