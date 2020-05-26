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
from pnlp import Reader

DATA_PATH = "./pnlp/tests/piop_data/"
pattern = '*.md' # also could be '*.txt', 'f*.*', etc.
reader = Reader(pattern)

# Get lines of all files in one directory with line index and file name
for line in reader(DATA_FOLDER_PATH):
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
# if a file is read, the `pattern` is not effective
for line in reader(os.path.join(DATA_FOLDER_PATH, "a.md")):
    print(line.lid, line.fname, line.text)
"""
0 a.md line 1 in a.
1 a.md line 2 in a.
2 a.md line 3 in a.
"""

# Get all filepaths in one directory
for path in reader.gen_files(DATA_PATH, pattern):
    print(path)
"""
pnlp/tests/piop_data/a.md
pnlp/tests/piop_data/first/fa.md
pnlp/tests/piop_data/first/second/sa.md
"""

# Get content(article) of all files in one directory with file name
paths = reader.gen_files(DATA_PATH, pattern)
articles = reader.gen_articles(paths)
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
paths = reader.gen_files(DATA_PATH, pattern)
articles = reader.gen_articles(paths)
for line in reader.gen_flines(articles):
    print(line.lid, line.fname, line.text)
```

#### Built-in Method

```python
import pnlp

# Read
file_string = pnlp.read_file(file_path)
file_list = pnlp.read_lines(file_path)
file_json = pnlp.read_json(file_path)
file_yml = pnlp.read_yml(file_path)

# Write
pnlp.write_json(file_path, data)
pnlp.write_file(file_path, data)

# Others
pnlp.check_dir(dirname) # will make dirname if not exist
```

### Text

#### Clean and Extract

```python
import re

# Use Text
from pnlp import Text

text = "这是https://www.yam.gift长度测试，《 》*)FSJfdsjf😁![](http://xx.jpg)。233."
pattern = re.compile(r'\d+')

# pattern is re.Pattern or str type
# Default is '', means do not use any pattern (acctually is re.compile(r'.+'). In this pattern, clean returns nothing, extract returns the origin.
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

pt = Text(['chi', pattern])
# pt.extract will return matches and their locations
res = pt.extract(text)

print(res)
"""
{'text': '这是长度测试233', 'mats': ['这是', '长度测试', '233'], 'locs': [(0, 2), (22, 26), (60, 63)]}
"""

print(res.text, res.mats, res.locs)
"""
'这是长度测试' ['这是', '长度测试'] [(0, 2), (22, 26)]
"""
# pt.clean will return cleaned text using the pattern
print(pt.clean(text))
"""
https://www.yam.gift，《 》*)FSJfdsjf😁![](http://xx.jpg)。233.
"""

pt = Text(['pic', 'lnk'])
res = pt.extract(text)

print(res.mats)
"""
['https://www.yam.gif',
 '![](http://xx.jpg)',
 'https://www.yam.gift',
 'http://xx.jpg']
"""

print(pt.clean(text))
"""
这是t长度测试，《 》*)FSJfdsjf😁。233.
"""
```

#### Regex

```python
# USE Regex
from pnlp import Regex
reg = Regex()
def clean_text(text: str) -> str:
    text = reg.pwhi.sub("", text)
    text = reg.pemj.sub("", text)
    text = reg.ppic.sub("", text)
    text = reg.plnk.sub("", text)
    return text
```

#### SentenceCut

```python
# Cut Sentence
from pnlp import cut_sentence as pcs
text = "你好！欢迎使用。"
sent_list = pcs(text)
print(sent_list)
"""
['你好！', '欢迎使用。']
"""
```

### Length

```python
from pnlp import Length

text = "这是https://www.yam.gift长度测试，《 》*)FSJfdsjf😁![](http://xx.jpg)。233."

pl = Length(text)
# Note that even a pattern is used, the length is always for the raw text.
# Length is counted by character, not entire word or number.
print("Length of all characters: ", pl.len_all)
print("Length of all non-white characters: ", pl.len_nwh)
print("Length of all Chinese characters: ", pl.len_chi)
print("Length of all words and numbers: ", pl.len_wnb)
print("Length of all punctuations: ", pl.len_pun)
print("Length of all English characters: ", pl.len_eng)
print("Length of all numbers: ", pl.len_num)

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
from pnlp import MagicDict

# Nest dict
pmd = MagicDict()
pmd['a']['b']['c'] = 2
print(pmd)

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
$ pytest
```

## ChangeLog

### v0.24

Add `stop_words`. Fix `read_json`.

### v0.23

Fix `Text` default rule.

### v0.22

Make `Text` more convenient to use.

### v0.21

Add `cut_sentence` method.

### v0.20

Optimize several interface and make `Text` accept list of Regular Expression Patterns.

