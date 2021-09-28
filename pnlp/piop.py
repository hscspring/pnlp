# from __future__ import annotations

from addict import Dict
import json
import pickle
import os
import re
import csv
import pathlib
import yaml


class Reader:
    """
    Parameters
    -----------
    pattern: path pattern, support Regex. default "*.*"
    use_regex: whether to use Regex to compile the string pattern. default False
    """

    def __init__(self, pattern: str = "*.*", use_regex: bool = False):
        self.pattern = pattern
        self.use_regex = use_regex

    def __repr__(self) -> str:
        return "Reader(pattern=%r)" % (self.pattern)

    @staticmethod
    def gen_files(dirname: str, pattern: str = "*.*", use_regex: bool = False):
        """
        Find all filenames in a directory tree that match the filepattern.
        If filepath is a file, yield the filepath directly.
        """
        if os.path.isfile(dirname):
            fpath = pathlib.Path(dirname)
            yield fpath
        if use_regex:
            try:
                pat = re.compile(pattern)
            except Exception:
                raise ValueError("hnlp: invalid pattern: {}".format(pattern))

            for fpath in pathlib.Path(dirname).rglob("*.*"):
                if pat.search(fpath.name):
                    yield fpath
        else:
            for fpath in pathlib.Path(dirname).rglob(pattern):
                yield fpath

    @staticmethod
    def gen_articles(fpaths: list):
        for fpath in fpaths:
            with open(fpath, encoding="utf8") as f:
                article = Dict()
                article.fname = fpath.name
                article.f = f
                yield article

    @staticmethod
    def gen_flines(articles: list, strip: str = "\n"):
        """
        Process each file to lines when io.TextIOWrapper is given.
        """
        for article in articles:
            lid = 0
            for line_content in article.f:
                line_content = line_content.strip(strip)
                if len(line_content) == 0:
                    continue
                line = Dict()
                line.lid = lid
                line.fname = article.fname
                line.text = line_content
                lid += 1
                yield line

    @staticmethod
    def gen_plines(fpath: str, strip: str = "\n"):
        """
        Process each file to lines when fpath is given.
        """
        with open(fpath, encoding="utf8") as f:
            for line in f:
                line = line.strip(strip)
                if len(line) == 0:
                    continue
                yield line

    def __call__(self, dirname: str):
        fpaths = Reader.gen_files(dirname, self.pattern, self.use_regex)
        articles = Reader.gen_articles(fpaths)
        flines = Reader.gen_flines(articles)
        for line in flines:
            yield line


def read_file(fpath: str, **kwargs) -> str:
    """
    Read file from file path.

    Parameters
    -----------
    fpath: str
        File path.
    kwargs: optional
        Other `open` support params.

    Returns
    --------
        data string of the file.
    """
    with open(fpath, **kwargs) as f:
        data = f.read()
    return data


def read_lines(fpath: str, strip: str = "\n", **kwargs) -> list:
    """
    Read file with `open` from file path.

    Parameters
    ----------
    fpath: str
        File path.
    strip: str
        Strip method, could be "both", "left", "right" or None.
    kwargs: optional
        Other `open` support params.

    Returns
    -------
    Lines of the file.

    Notes
    -----
    Blank line is ignored as default.
    """
    res = []
    with open(fpath, **kwargs) as f:
        for line in f:
            line = line.strip(strip)
            if len(line) == 0:
                continue
            res.append(line)
    return res


def read_csv(fpath: str, delimiter: str = ","):
    data = []
    with open(fpath, "r") as f:
        fcsv = csv.reader(f, delimiter=delimiter)
        for row in fcsv:
            data.append(row)
    return data


def read_json(fpath: str, **kwargs):
    with open(fpath, "r") as fin:
        data = json.load(fin, **kwargs)
    return data


def read_yaml(fpath: str):
    with open(fpath, "r") as fin:
        data = yaml.load(fin, Loader=yaml.SafeLoader)
    return data


def write_json(fpath: str, data, **kwargs):
    fout = open(fpath, "w")
    kwargs["ensure_ascii"] = False
    json.dump(data, fout, **kwargs)
    fout.close()


def write_file(fpath: str, data, **kwargs):
    with open(fpath, "w", **kwargs) as fout:
        for line in data:
            fout.write(line + "\n")


def read_pickle(fpath: str, **kwargs):
    with open(fpath, "rb") as f:
        data = pickle.load(f, **kwargs)
    return data


def write_pickle(fpath: str, data, **kwargs):
    with open(fpath, "wb") as f:
        pickle.dump(data, f, **kwargs)


def check_dir(dirname: str):
    if os.path.exists(dirname):
        pass
    else:
        os.makedirs(dirname)
