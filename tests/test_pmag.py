from pnlp.pmag import MagicDict


def test_magic():
    tmd = MagicDict()
    tmd["a"]["b"]["c"] = 1
    assert tmd["a"]["b"]["c"] == 1


def test_magic_set_get():
    d = MagicDict()
    d["a"]["b"] = 2
    assert d.a.b == 2


def test_magic_reverse():
    dx = {1: "a", 2: "a", 3: "a", 4: "b"}
    assert MagicDict.reverse(dx) == {"a": [1, 2, 3], "b": 4}
