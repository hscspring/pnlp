import re
from .ptxt import Regex
from .utils import pstr


psent = re.compile(r'''
    [。.！!?？…]+[”][。.!?！？…]?
    |
    (?<=[a-zA-Z"”》）)〉〕】>」』\u4e00-\u9fa5])[.。！!?？…～~]+
    ''', re.UNICODE | re.VERBOSE)
# referenced from jieba
punzh = pstr(Regex.pun_zh) - "-"
re_zh = re.compile(rf"([\u4E00-\u9FD5{punzh}+#&_]+)", re.UNICODE)
re_skip = re.compile(r"(\s)", re.UNICODE)


def cut_zhchar(text: str, remove_blank: bool = False) -> list:
    lst = []
    blocks = re_zh.split(text)
    for block in blocks:
        if not block:
            continue
        if re_zh.match(block):
            for char in block:
                lst.append(char)
        else:
            skips = re_skip.split(block)
            for skip in skips:
                if remove_blank:
                    skip = re_skip.sub("", skip)
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
