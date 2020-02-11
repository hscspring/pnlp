from .piop import Reader
from .piop import read_file, read_lines, read_json, read_yml
from .piop import write_file, write_json, check_dir
from .ptxt import Text, Regex
from .pmag import MagicDict


__title__ = 'pnlp'
__version__ = '0.2'
__author__ = 'Yam'
__license__ = 'MIT'
__copyright__ = 'Copyright 2019, 2020 Yam'
__all__ = ['Reader', 'Text', 'Regex', 'MagicDict']
