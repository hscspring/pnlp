from functools import wraps, partial
from typing import Any, List, Generator, Callable
import multiprocessing as mp
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import numpy as np
import dill


class pstr(str):
    def __sub__(self, other) -> str:
        result = []
        for c in self:
            if c in other:
                continue
            result.append(c)
        return "".join(result)


class ThreadWithReturnValue(Thread):
    """
    referenced from https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
    """

    def __init__(
            self,
            group=None,
            target=None,
            name=None,
            args=(),
            kwargs={}
    ):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def divide2int1(y: int, x: int) -> int:
    res = y // x
    if y % x != 0:
        res += 1
    return res


def divide2int(y: int, x: int) -> int:
    return np.ceil(y / x).astype(np.int_)


def generate_batches_by_size(lst: List[Any], batch_size: int
                             ) -> Generator[List[Any], None, None]:
    batch_num = divide2int(len(lst), batch_size)
    for i in range(batch_num):
        yield lst[i * batch_size: (i + 1) * batch_size]


def generate_batches_by_num(lst: List[Any], batch_num: int
                            ) -> Generator[List[Any], None, None]:
    batch_size = divide2int(len(lst), batch_num)
    return generate_batches_by_size(lst, batch_size)


# referenced from:
# https://izziswift.com/python-multiprocessing-picklingerror-cant-pickle/
def run_dill_encoded(payload):
    fun, args, kwargs = dill.loads(payload)
    return fun(*args, **kwargs)


def apply_async(pool, fun, args, kwargs):
    payload = dill.dumps((fun, args, kwargs))
    return pool.apply_async(run_dill_encoded, (payload,))


def concurring(
        func=None,
        type: str = "thread_executor",
        max_workers: int = mp.cpu_count()
) -> Generator[List[Any], None, None]:
    """
    decorator for concurring.

    Parameters
    -----------
    type: one of thread_pool, process_pool, thread_executor, thread
        these are all different implements.
    max_workers: worker number
    """

    if func is None:
        return partial(concurring, type=type, max_workers=max_workers)

    if max_workers <= 0:
        raise ValueError("hnlp: max_workers must > 0")

    def _thread(engine, func, batches, **kwargs):
        jobs = []
        for batch in batches:
            job = engine(target=func, args=(batch, ), kwargs=kwargs)
            jobs.append(job)
            job.start()
        for i, job in enumerate(jobs):
            yield job.join()

    def _pool(engine, func, batches, max_workers, **kwargs):
        with engine(processes=max_workers) as pool:
            jobs = [apply_async(pool, func, (batch, ), kwargs)
                    for batch in batches]
            for job in jobs:
                yield job.get()

    def _executor(engine, func, batches, max_workers, **kwargs):
        with engine(max_workers=max_workers) as executor:
            jobs = [executor.submit(*(func, batch), **kwargs)
                    for batch in batches]
            for f in jobs:
                yield f.result()

    @wraps(func)
    def wrapper(lst: List[Any], *args, **kwargs):
        batches = generate_batches_by_num(lst, max_workers)
        if type == "thread_pool":
            return _pool(
                ThreadPool, func, batches, max_workers, **kwargs)
        elif type == "process_pool":
            return _pool(
                Pool, func, batches, max_workers, **kwargs)
        elif type == "thread_executor":
            return _executor(
                ThreadPoolExecutor, func, batches, max_workers, **kwargs)
        elif type == "thread":
            return _thread(
                ThreadWithReturnValue, func, batches, **kwargs)
        else:
            err_info = f"hnlp: does not support type {type}, use one of "
            err_info += "thread_pool, process_pool, thread_executor, thread"
            raise ValueError(err_info)

    return wrapper
