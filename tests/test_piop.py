import os
import pytest
import types

from pnlp.piop import write_json, write_file
from pnlp.piop import Reader, read_file, read_lines, read_json, read_yaml, read_csv
from pnlp.piop import read_file_to_list_dict, write_list_dict_to_file
from pnlp.piop import check_dir

DATA_PATH = os.path.join('tests', 'piop_data')


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
    assert isinstance(paths, types.GeneratorType)
    assert len(list(paths)) == 3


def test_Reader_gen_files_with_regex():
    paths = Reader.gen_files(DATA_PATH, "(md)|(txt)", True)
    assert isinstance(paths, types.GeneratorType)
    assert len(list(paths)) == 6


def test_Reader_gen_articles():
    paths = Reader.gen_files(DATA_PATH, '*.txt')
    articles = Reader.gen_articles(paths)
    assert isinstance(articles, types.GeneratorType)
    assert len(list(articles)) == 3


def test_Reader_gen_flines():
    paths = Reader.gen_files(DATA_PATH, '*.txt')
    articles = Reader.gen_articles(paths)
    lines = Reader.gen_flines(articles)
    assert isinstance(lines, types.GeneratorType)
    assert len(list(lines)) == 9


def test_Reader_gen_plines():
    lines = Reader.gen_plines(os.path.join(DATA_PATH, 'b.txt'))
    assert isinstance(lines, types.GeneratorType)
    assert len(list(lines)) == 3


@pytest.fixture
def get_read_data():
    return os.path.join(DATA_PATH, 'c.data')


def test_read_file(get_read_data):
    data = read_file(get_read_data)
    assert data == 'line 1 in c.\nline 2 in c.\nline 3 in c.'
    assert type(data) == str


@pytest.mark.parametrize("count", [0, 1, 2, -1])
def test_read_lines(get_read_data, count):
    data = read_lines(get_read_data, count=count)
    if count != -1:
        assert len(data) == count
    else:
        assert data == ['line 1 in c.', 'line 2 in c.', 'line 3 in c.']
    assert type(data) == list


def test_read_json():
    data = read_json(os.path.join(DATA_PATH, 'json.json'))
    assert type(data) == dict
    assert data == {
        "json1": "this is line 1",
        "json2": "这是第二行。"
    }


def test_read_yaml():
    data = read_yaml(os.path.join(DATA_PATH, 'yaml.yaml'))
    assert type(data) == dict
    assert data == {'元旦': ['新年快乐', '元旦快乐', '节日快乐'],
                    '周末': ['周末快乐！', '周末愉快！']}


def test_read_csv():
    data = read_csv(os.path.join(DATA_PATH, 'csv.csv'))
    assert type(data) == list
    assert data == [['id', 'title'], ['1', 'title1'], ['2', 'title2']]


def test_read_file_to_list_dict():
    data = read_file_to_list_dict(os.path.join(DATA_PATH, "list_dict.json"))
    assert type(data) == list
    assert type(data[0]) == dict


def test_write_json():
    data = {"outjson1": "this is line 1.",
            "outjson2": "这是第二行。"}
    write_json(os.path.join(DATA_PATH, 'outjson.json'),
               data, indent=4, ensure_ascii=False)


def test_write_file():
    data = ['line 1 of outfile.', '这是 outfile 的第二行。']
    write_file(os.path.join(DATA_PATH, 'outfile.file'), data)


def test_write_list_dict_to_file():
    data = [{"name": "Yam", "age": 20}]
    write_list_dict_to_file(os.path.join(DATA_PATH, "outfile.listdict"), data)


def test_check_dir():
    assert check_dir(DATA_PATH) is None
