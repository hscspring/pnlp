from functools import wraps, partial
from typing import Any, List, Generator
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


class pstr(str):
    def __sub__(self, other) -> str:
        result = []
        for c in self:
            if c in other:
                continue
            result.append(c)
        return "".join(result)


def divide2int(y: int, x: int) -> int:
    res = y // x
    if y % x != 0:
        res += 1
    return res


def generate_batches_by_size(lst: List[Any], batch_size: int
) -> Generator[List[Any], None, None]:
    batch_num = divide2int(len(lst), batch_size)
    for i in range(batch_num):
        yield lst[i*batch_size: (i+1)*batch_size]


def generate_batches_by_num(lst: List[Any], batch_num: int
) -> Generator[List[Any], None, None]:
    batch_size = divide2int(len(lst), batch_num)
    return generate_batches_by_size(lst, batch_size)


def concurring(
        func=None, type: str = "thread", max_workers: int = mp.cpu_count()
) -> Generator[List[Any], None, None]:

    if func is None:
        return partial(concurring, type=type, max_workers=max_workers)

    if type == "thread":
        engine = ThreadPoolExecutor
    elif type == "process":
        engine = ProcessPoolExecotor
    else:
        err_info = f"hnlp: does not support type {type}. "
        err_info += "please use 'thread' or 'process'"
        raise ValueError(err_info)

    @wraps(func)
    def wrapper(lst: List[Any], *args, **kwargs):
        with engine(max_workers) as executor:
            futures = [executor.submit(func, batch, *args, *kwargs)
                       for batch in generate_batches_by_num(lst, max_workers)]
            for f in futures:
                yield f.result()
    return wrapper


def strip_text(text: str, strip: str):
    if strip == "both":
        return text.strip()
    elif strip == "left":
        return text.lstrip()
    elif strip == "right":
        return text.rstrip()
    else:
        return text
