import os
import sys
import pytest
import types

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

from piop import write_json, write_file
from piop import Reader, read_file, read_lines, read_json, read_yml
from piop import check_dir

DATA_PATH = os.path.join(ROOT_PATH, 'tests', 'piop_data')


@pytest.fixture(params=['*.md', '*.txt', '*.data', 'f*.*', '*c.*'])
def get_Reader_path_match_res(request):
    res = []
    reader = Reader(request.param)
    for line in reader(DATA_PATH):
        res.append(line)
    return res


def test_Reader_path_match(get_Reader_path_match_res):
    assert len(get_Reader_path_match_res) == 9
    assert get_Reader_path_match_res[0].lid == 0
    assert get_Reader_path_match_res[-1].lid == 2


def test_Reader_file():
    res = []
    reader = Reader()
    for line in reader(os.path.join(DATA_PATH, 'a.md')):
        res.append(line)
    assert len(res) == 3
    assert res[0].text == 'line 1 in a.'


def test_Reader_gen_files():
    paths = Reader.gen_files(DATA_PATH, '*.md')
    assert isinstance(paths, types.GeneratorType) == True
    assert len(list(paths)) == 3


def test_Reader_gen_articles():
    paths = Reader.gen_files(DATA_PATH, '*.txt')
    articles = Reader.gen_articles(paths)
    assert isinstance(articles, types.GeneratorType) == True
    assert len(list(articles)) == 3


def test_Reader_gen_flines():
    paths = Reader.gen_files(DATA_PATH, '*.txt')
    articles = Reader.gen_articles(paths)
    lines = Reader.gen_flines(articles)
    assert isinstance(lines, types.GeneratorType) == True
    assert len(list(lines)) == 9


def test_Reader_gen_plines():
    lines = Reader.gen_plines(os.path.join(DATA_PATH, 'b.txt'))
    assert isinstance(lines, types.GeneratorType) == True
    assert len(list(lines)) == 3


@pytest.fixture
def get_read_data():
    return os.path.join(DATA_PATH, 'c.data')


def test_read_file(get_read_data):
    data = read_file(get_read_data)
    assert data == 'line 1 in c.\nline 2 in c.\nline 3 in c.'
    assert type(data) == str


def test_read_lines(get_read_data):
    data = read_lines(get_read_data)
    assert data == ['line 1 in c.', 'line 2 in c.', 'line 3 in c.']
    assert type(data) == list


def test_read_json():
    data = read_json(os.path.join(DATA_PATH, 'json.json'))
    assert type(data) == dict
    assert data == {
        "json1": "this is line 1",
        "json2": "这是第二行。"
    }


def test_read_yml():
    data = read_yml(os.path.join(DATA_PATH, 'yml.yml'))
    assert type(data) == dict
    assert data == {'元旦': ['新年快乐', '元旦快乐', '节日快乐'],
                    '周末': ['周末快乐！', '周末愉快！']}


def test_write_json():
    data = {"outjson1": "this is line 1.",
            "outjson2": "这是第二行。"}
    write_json(os.path.join(DATA_PATH, 'outjson.json'),
               data, indent=4, ensure_ascii=False)


def test_write_file():
    data = ['line 1 of outfile.', '这是 outfile 的第二行。']
    write_file(os.path.join(DATA_PATH, 'outfile.file'), data)

def test_check_dir():
    assert check_dir(DATA_PATH) == None


if __name__ == '__main__':
    print(ROOT_PATH)
    print(IODATA_PATH)
