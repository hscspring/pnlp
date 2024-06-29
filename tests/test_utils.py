import re
import os
from functools import partial
import math
import itertools
import pytest
import multiprocessing as mp

from pnlp.utils import pstr, concurring, generate_batches_by_num
from pnlp.utils import run_in_new_thread
from pnlp.piop import read_file, write_file


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


def test_generate_batches():
    lst = range(100)
    res = list(generate_batches_by_num(lst, 10))
    assert len(res) == 10
    assert len(res[0]) == 10


def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True


def test_concurring_default():

    @concurring
    def get_primes(lst):
        res = []
        for i in lst:
            if is_prime(i):
                res.append(i)
        return res
    lst = list(range(100))
    res = get_primes(lst)
    res = list(res)
    assert len(res) == mp.cpu_count()
    res = list(itertools.chain(*res))
    assert len(res) == 25


@pytest.mark.parametrize(
    "type",
    ["thread_pool", "process_pool", "thread_executor", "thread"])
@pytest.mark.parametrize("max_workers", [1, 2, 4, 7, 10])
def test_concurring_with_parameters(type, max_workers):

    @concurring(type=type, max_workers=max_workers)
    def get_primes(lst):
        res = []
        for i in lst:
            if is_prime(i):
                res.append(i)
        return res
    lst = list(range(100))
    res = get_primes(lst)
    res = list(res)
    assert len(res) == max_workers
    res = list(itertools.chain(*res))
    assert len(res) == 25


def test_concurring_invalid_type():

    @concurring(type="invalid")
    def get_primes(lst):
        res = []
        for i in lst:
            if is_prime(i):
                res.append(i)
        return res
    lst = list(range(100))
    try:
        res = get_primes(lst)
    except Exception as err:
        assert "invalid" in str(err)


def test_concurring_invalid_workers():

    try:
        @concurring(max_workers=0)
        def get_primes(lst):
            res = []
            for i in lst:
                if is_prime(i):
                    res.append(i)
            return res
    except Exception as err:
        assert "0" in str(err)



def test_run_in_thread():
    file = "run_in_new_thread.txt"
    
    def func(file, a, b, c):
        write_file(file, list(map(str, [a, b, c])))

    run_in_new_thread(func, file, 1, 2, 3)
    import time
    time.sleep(1)

    assert os.path.exists(file)
    os.remove(file)


def test_run_in_thread_kwargs():
    kwargs = {
        "b": 2,
        "c": 3,
    }

    def func(a, b, c):
        return a + b + c

    func = partial(func, **kwargs)

    assert 6 == func(1)

