from .piop import Reader, Dict
from .piop import read_file, read_lines, read_json, read_yaml, read_csv
from .piop import write_file, write_json, check_dir
from .ptxt import Regex, Text, Length
from .pcut import cut_sentence, cut_zhchar, cut_part, combine_bucket
from .pcut import psent, psubsent
from .pnorm import NumNorm
from .pmag import MagicDict

from .utils import pstr

from .stopwords import chinese_stopwords, english_stopwords, StopWords


num_norm = NumNorm()
reg = Regex()
reader = Reader()


__title__ = 'pnlp'
__version__ = '0.3.4'
__author__ = 'Yam'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2019, 2020 Yam'
__all__ = ['Reader', 'Text', 'Regex', 'Length', 'MagicDict', 'NumNorm']

