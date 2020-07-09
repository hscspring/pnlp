import re
from .ptxt import Regex
from .utils import pstr


psent = re.compile(r'''
    \n+
    |
    [。.！!?？…]+[”][。.!！?？…～~]?
    |
    (?<=[a-zA-Z"”》）)〉〕】>」』\u4e00-\u9fa5])[。.!！?？…～~]+
    ''', re.UNICODE | re.VERBOSE)
# referenced from jieba
punzh = pstr(Regex.pun_zh) - "-"  # for minus number eg -2
punen = pstr(Regex.pun_en) - "."  # for float number eg 1.3
pun = punzh + punen
pzh = re.compile(rf"([\u4E00-\u9FD5{pun}+#&])", re.UNICODE)
pen = re.compile(r"([a-zA-Z]+)", re.UNICODE)
pskip = re.compile(r"(\s)", re.UNICODE)
pspecial = re.compile(r"([-.])")  # split to single
pnum = re.compile(r"""
    ([-]?\d{1,}[.]?\d{0,}%)
    |
    ([-]?\d{1,}[./]?\d{0,})    
    """, re.UNICODE | re.VERBOSE)


def cut_zhchar(text: str, remove_blank: bool = False) -> list:
    lst = []
    blocks = pzh.split(text)
    for block in blocks:
        if not block:
            continue
        if pzh.match(block):
            for char in block:
                lst.append(char)
        else:
            skips = pskip.split(block)
            for skip in skips:
                if pen.search(skip):
                    for en_part in pen.split(skip):
                        if en_part:
                            spe = pspecial.search(en_part)
                            if not spe:
                                lst.append(en_part)
                            else:
                                for spe_part in pspecial.split(en_part):
                                    if spe_part:
                                        lst.append(spe_part)
                elif pnum.search(skip):
                    if skip[-1] != ".":
                        lst.append(skip)
                    else:
                        i = 0
                        while skip[-1] == ".":
                            i += 1
                            skip = skip[:-1]
                        lst.append(skip)
                        for _ in range(i):
                            lst.append(".")
                else:
                    if remove_blank:
                        skip = pskip.sub("", skip)
                    if skip:
                        lst.append(skip)
    return lst


def cut_sentence(text: str) -> list:
    ends = psent.findall(text)
    length = len(ends)
    lst = []
    for i, sent in enumerate(psent.split(text)):
        if i < length:
            sent = sent + ends[i]
        if sent:
            lst.append(sent)
    return lst
