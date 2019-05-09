# pnlp
This is a pre-processing tool for NLP.

## Features

- a flexible pipe line for text io
- a flexible tool for text clean and extract and kinds of length
- some magic usage in pre-processing

## Install

`pip install pnlp`

## Usage

### Iopipe

#### IO process

```bash
tree tests/piop_data/
├── a.md
├── b.txt
├── c.data
├── first
│   ├── fa.md
│   ├── fb.txt
│   ├── fc.data
│   └── second
│       ├── sa.md
│       ├── sb.txt
│       └── sc.data
├── json.json
├── outfile.file
├── outjson.json
└── yml.yml
```

```python
import os
from pnlp import piop

DATA_PATH = "./pnlp/tests/piop_data/"
pattern = '*.md' # also could be '*.txt', 'f*.*', etc.

# Get lines of all files in one directory with line index and file name
for line in piop.Reader(DATA_PATH, pattern):
    print(line.lid, line.fname, line.text)
"""
0 a.md line 1 in a.
1 a.md line 2 in a.
2 a.md line 3 in a.
0 fa.md line 1 in fa.
1 fa.md line 2 in fa
...
"""

# Get lines of one file lines with line index and file name
for line in piop.Reader(os.path.join(DATA_PATH, "a.md")):
    print(line.lid, line.fname, line.text)
"""
0 a.md line 1 in a.
1 a.md line 2 in a.
2 a.md line 3 in a.
"""

# Get all filepaths in one directory
for path in piop.Reader.gen_files(DATA_PATH, pattern):
    print(path)
"""
pnlp/tests/piop_data/a.md
pnlp/tests/piop_data/first/fa.md
pnlp/tests/piop_data/first/second/sa.md
"""

# Get content(article) of all files in one directory with file name
paths = piop.Reader.gen_files(DATA_PATH, pattern)
articles = piop.Reader.gen_articles(paths)
for article in articles:
    print(article.fname)
    print(article.f.read())
"""
a.md
line 1 in a.
line 2 in a.
line 3 in a.
...
"""

# Get lines of all files in one directory with line index and file name
# the same as ip.Reader(DATA_PATH, pattern)
paths = piop.Reader.gen_files(DATA_PATH, pattern)
articles = piop.Reader.gen_articles(paths)
for line in piop.Reader.gen_flines(articles):
    print(line.lid, line.fname, line.text)
```

#### Built-in Method

```python
from pnlp import piop

# Read
file_string = piop.read_file(file_path)
file_list = piop.read_lines(file_path)
file_json = piop.read_json(file_path)
file_yml = piop.read_yml(file_path)

# Write
piop.write_json(file_path, data)
piop.write_file(file_path, data)

# Others
piop.check_dir(dirname) # will make dirname if not exist
```

### Text

#### Clean and Extract

```python
import re
from pnlp import ptxt

text = "这是https://www.yam.gift长度测试，《 》*)FSJfdsjf😁![](http://xx.jpg)。233."
pattern = re.compile(r'\w+')

# pattern is re.Pattern or str type
# Default is '', means do not use any pattern (acctually is re.compile(r'.+')
# If pattern is a string, a build-in pattern will be used, there are 11 types:
#	'chi': Chinese character
#	'pun': Punctuations
#	'whi': White space
#	'nwh': Non White space
#	'wnb': Word and number
#	'nwn': Non word and number
#	'eng': English character
#	'num': Number
#	'pic': Pictures
#	'lnk': Links
#	'emj': Emojis

pt = ptxt.Text(text, pattern)
# pt.extract will return matches and their locations
print(pt.extract)
"""
{'mats': ['这是', '长度测试'], 'locs': [(0, 2), (22, 26)]}
"""
print(pt.extract.mats, pt.extract.locs)
"""
['这是', '长度测试'] [(0, 2), (22, 26)]
"""
# pt.clean will return cleaned text using the pattern
print(pt.clean)
"""
https://www.yam.gift，《 》*)FSJfdsjf😁![](http://xx.jpg)。233.
"""
```

#### Length

```python
from pnlp import ptxt

text = "这是https://www.yam.gift长度测试，《 》*)FSJfdsjf😁![](http://xx.jpg)。233."

pt = ptxt.Text(text)
# Note that even a pattern is used, the length is always for the raw text.
# Length is counted by character, not entire word or number.
print("Length of all characters: ", pt.len_all)
print("Length of all non-white characters: ", pt.len_nwh)
print("Length of all Chinese characters: ", pt.len_chi)
print("Length of all words and numbers: ", pt.len_wnb)
print("Length of all punctuations: ", pt.len_pun)
print("Length of all English characters: ", pt.len_eng)
print("Length of all numbers: ", pt.len_num)
"""
Length of all characters:  64
Length of all non-white characters:  63
Length of all Chinese characters:  6
Length of all words and numbers:  41
Length of all punctuations:  14
Length of all English characters:  32
Length of all numbers:  3
"""
```

### Magic

```python
from pnlp import pmag

# Nest dict
dict1 = pmag.MagicDict()
dict1['a']['b']['c'] = 2
print(dict1)
"""
{'a': {'b': {'c': 2}}}
"""

# Preserve all repeated value-keys when a Dict is reversed.
dx = {1: 'a',
      2: 'a',
      3: 'a',
      4: 'b' }
print(pmag.MagicDict.reverse(dx))
"""
{'a': [1, 2, 3], 'b': 4}
"""
```

## Test

Clone the repo and enter the tests directory: 

```bash
cd ./pnlp/tests
pytest
```

