from pnlp.stopwords import StopWords



def test_stopwords():
    sw = StopWords()
    assert type(sw.zh) == set
    assert type(sw.en) == set
    assert sw.zh_len > 0
    assert sw.en_len > 0


def test_custom_stopwords():
    sw = StopWords("tests/piop_data/b.txt")
    assert type(sw.stopwords) == set
    assert len(sw.stopwords) == 3