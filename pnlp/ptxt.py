# from __future__ import annotations
from addict import Dict
import re


class Text:

    """
    Text clean, extract and length.

    Parameters
    ----------
    text: str
        Raw text.
    pat: re.Pattern or str
        Support custom re.Pattern. 
        Default is '', will use re.compile(r'.+').
        Other str pattern is built-in, including:
        'chi': Chinese character
        'pun': Punctuations
        'whi': White space
        'nwh': Non White space
        'wnb': Word and number
        'nwn': Non word and number
        'eng': English character
        'num': Number
        'pic': Pictures
        'lnk': Links
        'emj': Emojis

    Returns
    -------
    A text object.
    """

    def __init__(self, text: str, pat: str or re.Pattern = ''):
        self.text = text
        self.reg = Regex()
        if isinstance(pat, str):
            self.pat = self.reg.patdict.get(pat, re.compile(r'.+'))
        else:
            self.pat = pat

    def __repr__(self) -> str:
        attrs = self.text if len(self.text) <= 10 else self.text[:10] + "..."
        return "Text(text=%r)" % (attrs)

    @property
    def clean(self):
        """
        Clean text with givening pattern.

        Returns
        -------
        Cleaned text.
        """
        text = self.pat.sub("", self.text)
        return text

    @property
    def extract(self):
        """
        Extract pattern-matching items.

        Returns
        -------
        Extracted items and their locations.
        """
        mats = []
        locs = []
        for mat in self.pat.finditer(self.text):
            mats.append(mat.group())
            locs.append(mat.span())
        ext = Dict()
        ext.mats = mats
        ext.locs = locs
        return ext

    def _len(self, pat):
        lst = pat.findall(self.text)
        return len("".join(lst))

    @property
    def len_all(self):
        """
        Length of all characters.
        """
        return len(self.text)

    @property
    def len_nwh(self):
        """
        Length of non-white characters.
        """
        return self._len(self.reg.pnwh)

    @property
    def len_chi(self):
        """
        Length of pure Chinese characters.
        """
        return self._len(self.reg.pchi)

    @property
    def len_wnb(self):
        """
        Length of characters and numbers.
        """
        return self._len(self.reg.pwnb)

    @property
    def len_pun(self):
        """
        Length of all punctuations.
        """
        return self._len(self.reg.ppun)

    @property
    def len_eng(self):
        """
        Length of English characters.
        """
        return self._len(self.reg.peng)

    @property
    def len_num(self):
        """
        Length of all numbers.
        """
        return self._len(self.reg.pnum)


class Regex:

    """
    All kinds of Regular patterns.
    """

    patnames = ["chi", "pun", 
                "whi", "nwh", 
                "wnb", "nwn",
                "eng", "num", 
                "pic", "lnk", "emj"]

    pun_en = r"，。；、？！：“”‘’（）「」『』〔〕【】《》〈〉…——\-—～·"
    pun_zh = r",.;?!\(\)\[\]\{\}<>_"

    @property
    def pchi(self):
        """
        Chinese char pattern.
        """
        _pchi = re.compile(r'[\u4e00-\u9fa5]+')
        return _pchi

    @property
    def ppun(self):
        """
        Punctuation pattern.
        """
        _ppun = re.compile(rf'[{self.pun_en + self.pun_zh}]+')
        return _ppun

    @property
    def pwhi(self):
        """
        White space pattern.
        """
        _pwhi = re.compile(r'\s+')
        return _pwhi

    @property
    def pnwh(self):
        """
        Non-white space pattern.
        """
        _pnwh = re.compile(r'\S+')
        return _pnwh

    @property
    def pwnb(self):
        """
        Word and num pattern.
        """
        _pwnb = re.compile(r'\w+')
        return _pwnb

    @property
    def pnwn(self):
        """
        Non-alphanumeric char pattern.
        """
        _pnwn = re.compile(r'\W+')
        return _pnwn

    @property
    def peng(self):
        """
        English char pattern.
        """
        _peng = re.compile(r'[a-zA-Z]+')
        return _peng

    @property
    def pnum(self):
        """
        Number pattern.

        Example
        -------
        2, +2, -2, 2.1, -2.2, 1/5, 2:3, -2/5, 2%, 2.5%
        """
        _pnum = re.compile(r'''
                    [+-.]?\d+[.:/]?[\d%]+
                    |
                    [+-.]?\d+(?!\.\w+)
                    ''', re.UNICODE | re.VERBOSE)
        return _pnum

    @property
    def ppic(self):
        """
        Picture pattern.
        """
        _ppic = re.compile(r'''
                    !\[.*?\]\(.*?\.(jpeg|png|jpg|gif)\)
                    |
                    https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{0,256}\.(jpeg|png|jpg|gif)
                    ''', 
                    re.UNICODE | re.VERBOSE)
        return _ppic

    @property
    def plnk(self):
        """
        Link pattern.
        """
        _plink = re.compile(r'''
                    \[\w+?\]\(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{0,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)\)
                    |
                    https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{0,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)
                    ''', 
                    re.UNICODE | re.VERBOSE)
        return _plink

    @property
    def pemj(self):
        """
        Emoj pattern.
        """
        _pemj = re.compile(
            r'['u'\U0001F300-\U0001F64F'
                u'\U0001F680-\U0001F6FF'
                u'\u2600-\u2B55]+')
        return _pemj

    @property
    def patdict(self):
        """
        All patterns.
        """
        patterns = [self.pchi, self.ppun,
                    self.pwhi, self.pnwh, 
                    self.pwnb, self.pnwn,
                    self.peng, self.pnum,
                    self.ppic, self.plnk, self.pemj]
        _patdict = dict(zip(self.patnames, patterns))
        return _patdict


