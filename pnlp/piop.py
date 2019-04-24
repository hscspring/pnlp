# from __future__ import annotations

from addict import Dict
# from dataclasses import dataclass
import json
import os
import pathlib
import smart_open
import yaml


# @dataclass
class Reader:

    def __init__(self, dirname: str, pattern: str = "*.*"):
        self.dirname = dirname
        self.pattern = pattern

    def __repr__(self) -> str:
        return "Reader(dirname=%r, pattern=%r)" % (self.dirname, self.pattern)

    @staticmethod
    def gen_files(dirname: str, pattern: str = '*.*'):
        """
        Find all filenames in a directory tree that match the filepattern.
        If filepath is a file, yield the filepath directly.
        """
        if os.path.isfile(dirname):
            fpath = pathlib.Path(dirname)
            yield fpath
        for fpath in pathlib.Path(dirname).rglob(pattern):
            yield fpath

    @staticmethod
    def gen_articles(fpaths: list):
        for fpath in fpaths:
            with smart_open.open(fpath, encoding='utf8') as f:
                article = Dict()
                article.fname = fpath.name
                article.f = f
                yield article

    @staticmethod
    def gen_flines(articles: list):
        """
        Process each file to lines when io.TextIOWrapper is given.
        """
        for article in articles:
            lid = 0
            for line_content in article.f:
                line_content = line_content.strip()
                if len(line_content) == 0:
                    continue
                line = Dict()
                line.lid = lid
                line.fname = article.fname
                line.text = line_content
                lid += 1
                yield line

    @staticmethod
    def gen_plines(fpath: str):
        """
        Process each file to lines when fpath is given.
        """
        with smart_open.open(fpath, encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue
                yield line

    def __iter__(self):
        fpaths = self.gen_files(self.dirname, self.pattern)
        articles = self.gen_articles(fpaths)
        flines = self.gen_flines(articles)
        for line in flines:
            yield line


def read_file(fpath: str, **kwargs) -> str:
    """
    Read file with `smart_open` from file path.

    Parameters
    -----------
    fpath: str
        File path.
    kwargs: optional
        Other `smart_open` support params. 

    Returns
    --------
        data string of the file.
    """
    with smart_open.open(fpath, **kwargs) as f:
        data = f.read()
    return data


def read_lines(fpath: str, **kwargs) -> list:
    """
    Read file with `smart_open` from file path.

    Parameters
    ----------
    fpath: str
        File path.
    kwargs: optional
        Other `smart_open` support params. 

    Returns
    -------
    Lines of the file.

    Notes
    -----
    Blank line is ignored.
    """
    res = []
    with smart_open.open(fpath, **kwargs) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            res.append(line)
    return res


def read_json(fpath: str, **kwargs):
    fin = open(fpath, 'r')
    data = json.load(fin, **kwargs)
    return data


def read_yml(fpath: str):
    with open(fpath, 'r') as fin:
        data = yaml.load(fin, Loader=yaml.SafeLoader)
    return data


def write_json(fpath: str, data, **kwargs):
    fout = open(fpath, 'w')
    json.dump(data, fout, **kwargs)
    fout.close()


def write_file(fpath: str, data, **kwargs):
    with smart_open.open(fpath, 'w', **kwargs) as fout:
        for line in data:
            fout.write(line+"\n")


def check_dir(dirname: str):
    if os.path.exists(dirname):
        pass
    else:
        os.makedirs(dirname)


