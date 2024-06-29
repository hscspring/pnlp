import pytest
from pnlp.pmag import MagicDict, get_unique_fn


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



@pytest.mark.parametrize("inp,oup,level", [
    ("a.md", "a.md", 0),
    ("a.md", "a.md", 1),
    ("a.md", "a.md", 10),
    ("a/b.md", "a_b.md", 0),
    ("a/b.md", "a_b.md", 1),
    ("a/b.md", "a_b.md", 10),
    ("a/b/c.md", "a_b_c.md", 0),
    ("a/b/c.md", "b_c.md", 1),
    ("a/b/c.md", "a_b_c.md", 10),
    ("/a/b/c.md", "a_b_c.md", 0),
    ("/a/b/c.md", "b_c.md", 1),
    ("/a/b/c.md", "a_b_c.md", 10),
])
def test_get_unique_fn(inp, level, oup):
    res = get_unique_fn(inp, level)
    assert res == oup
