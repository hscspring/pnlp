import os
import sys
import pytest
import types

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)


from pmag import MagicDict


def test_MagicDict():
    tmd = MagicDict()
    tmd['a']['b']['c'] = 1
    assert tmd['a']['b']['c'] == 1

def test_MagicDict_reverse():
    dx = {  1: 'a', 2: 'a', 3: 'a', 4: 'b' }
    assert MagicDict.reverse(dx) == {  'a': [1, 2, 3], 'b': 4 }