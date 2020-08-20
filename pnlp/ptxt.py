from addict import Dict
import re


class Regex:

    """
    All kinds of Regular patterns.
    """

    patnames = ["chi", "pun",
                "whi", "nwh",
                "wnb", "nwn",
                "eng", "num",
                "pic", "lnk", "emj"]

    pun_zh = r"，。；、？！：“”‘’（）「」『』〔〕【】《》〈〉…——\-—～~·"
    pun_en = r",.;?!\(\)\[\]\{\}<>_"

    @property
    def pchi(self):
        """
        Chinese char pattern.
        """
        _pchi = re.compile(r'[\u4E00-\u9FD5]+')  # from jieba
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
                    !\[.*?\]\(.*?\.?(jpeg|png|jpg|gif)?\)
                    |
                    https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{0,256}\.(jpeg|png|jpg|gif)
                    ''', re.UNICODE | re.VERBOSE)
        return _ppic

    @property
    def plnk(self):
        """
        Link pattern.
        """
        _plink = re.compile(r'''
                    \[.+?\]\(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{0,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)\)
                    |
                    https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{0,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)
                    |
                    (https?:\/\/)?www\.[-a-zA-Z0-9@:%._\+~#=]{0,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)
                    ''', re.UNICODE | re.VERBOSE)
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


class Text(Regex):

    """
    Text clean, extract and length.

    Parameters
    ----------
    pat: list of patterns
        Support custom re.Pattern. 
        Default is re.compile(r'.+').
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

    Notes
    ------
    The pattern order is important. The front pattern will be excute earlier.
    """

    def __init__(self, pattern_list: list = []):
        self.pats = []
        for pat in pattern_list:
            if isinstance(pat, str):
                built_in_pat = self.patdict.get(pat)
                if built_in_pat:
                    self.pats.append(built_in_pat)
                else:
                    raise ValueError(
                        "pnlp: {} \
                        is not a valid built-in pattern.".format(pat))
            elif isinstance(pat, re.Pattern):
                self.pats.append(pat)
            else:
                raise ValueError(
                    "pnlp: {} is not a valid RE pattern.".format(pat))

    def __repr__(self) -> str:
        return "Text(pattern=%r)" % str(self.pat)

    def clean(self, text: str):
        """
        Clean text with givening pattern.

        Returns
        -------
        Cleaned text.
        """
        for pat in self.pats:
            text = pat.sub("", text)
        return text

    def extract(self, text: str):
        """
        Extract pattern-matching items.

        Returns
        -------
        Extracted items and their locations.
        """
        mats, locs = [], []
        for pat in self.pats:
            for mat in pat.finditer(text):
                mats.append(mat.group())
                locs.append(mat.span())
        ext = Dict()
        ext.text = "".join(mats)
        ext.mats = mats
        ext.locs = locs
        return ext


class Length(Regex):

    def __init__(self, text: str):
        self.text = text

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
        return self._len(self.pnwh)

    @property
    def len_chi(self):
        """
        Length of pure Chinese characters.
        """
        return self._len(self.pchi)

    @property
    def len_wnb(self):
        """
        Length of characters and numbers.
        """
        return self._len(self.pwnb)

    @property
    def len_pun(self):
        """
        Length of all punctuations.
        """
        return self._len(self.ppun)

    @property
    def len_eng(self):
        """
        Length of English characters.
        """
        return self._len(self.peng)

    @property
    def len_num(self):
        """
        Length of all numbers.
        """
        return self._len(self.pnum)
