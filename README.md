<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Features](#features)
- [Install](#install)
- [Usage](#usage)
  - [Iopipe](#iopipe)
    - [IO process](#io-process)
    - [Built-in Method](#built-in-method)
  - [Text](#text)
    - [Clean and Extract](#clean-and-extract)
    - [Regex](#regex)
  - [Cut](#cut)
    - [AnypartCut](#anypartcut)
    - [SentenceCut](#sentencecut)
    - [ChineseCharCut](#chinesecharcut)
    - [CombineBucket](#combinebucket)
  - [Enhancement](#enhancement)
  - [Normalization](#normalization)
  - [StopWords](#stopwords)
  - [Length](#length)
  - [Magic](#magic)
  - [Concurring](#concurring)
- [Test](#test)
- [ChangeLog](#changelog)
  - [v0.3.7](#v037)
  - [v0.3.5](#v035)
  - [v0.3.3/4](#v0334)
  - [v0.3.2](#v032)
  - [v0.3.1](#v031)
  - [v0.3.0](#v030)
  - [v0.28-29](#v028-29)
  - [v0.27](#v027)
  - [v0.26](#v026)
  - [v0.25](#v025)
  - [v0.24](#v024)
  - [v0.23](#v023)
  - [v0.22](#v022)
  - [v0.21](#v021)
  - [v0.20](#v020)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

This is a pre-processing tool for NLP.

## Features

- A flexible pipe line for text io
- A flexible tool for text clean and extract
- Text enhancement
- Sentence cut and Chinese character cut
- Text bucket
- Chinese character normalization
- Kinds of length
- Stopwords
- Some magic usage in pre-processing
- Tools like Concurring, generating batches

## Install

Need Python3.7+.

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
file_yaml = pnlp.read_yaml(file_path)
file_csv = pnlp.read_csv(file_path)

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

### Cut

#### AnypartCut

```python
# Cut by Regex
from pnlp import cut_part, psent
text = "你好！欢迎使用。"
sent_list = cut_part(text, psent, with_spliter=True, with_offset=False)
print(sent_list)
"""
['你好！', '欢迎使用。']
"""
pcustom_sent = re.compile(r'[。！]')
sent_list = cut_part(text, pcustom_sent, with_spliter=False, with_offset=False)
print(sent_list)
"""
['你好', '欢迎使用']
"""
sent_list = cut_part(text, pcustom_sent, with_spliter=False, with_offset=True)
print(sent_list)
"""
[('你好', 0, 3), ('欢迎使用', 3, 8)]
"""
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

#### ChineseCharCut

```python
# Cut to Chinese chars
from pnlp import cut_zhchar
text = "你好，hello, 520 i love u. = ”我爱你“。"
char_list = cut_zhchar(text)
print(char_list)
"""
['你', '好', '，', 'hello', ',', ' ', '520', ' ', 'i', ' ', 'love', ' ', 'u', '.', ' ', '=', ' ', '”', '我', '爱', '你', '“', '。']
"""
char_list = cut_zhchar(text, remove_blank=True)
print(char_list)
"""
['你', '好', '，', 'hello', ',', '520', 'i', 'love', 'u', '.', '=', '”', '我', '爱', '你', '“', '。']
"""
```

#### CombineBucket

```python
from pnlp import combine_bucket
parts = [
    '习近平指出',
    '中方不仅维护中国人民生命安全和身体健康',
    '也维护世界人民生命安全和身体健康',
    '我们本着公开',
    '透明'
]
buckets = combine_bucket(parts.copy(), 10, truncate=True, keep_remain=True)
print(buckets)
"""
['习近平指出', 
'中方不仅维护中国人民', 
'生命安全和身体健康', 
'也维护世界人民生命安', 
'全和身体健康', 
'我们本着公开透明']
"""
```

### Enhancement

```python
# Both Sampler support delete, swap and insert sampling method types.
text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
# TokenLevel
from pnlp import TokenLevelSampler
tls = TokenLevelSampler()
tls.make_samples(text)
"""
{'delete': '人为什么活着？生而为人必须要梦想！还要有尽可能多的精神体验。',
 'swap': '为人什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。',
 'insert': '人为什么活着？生而为人必须要有梦想！还还要有尽可能多的精神体验。',
 'together': '人什么着着活？生而必为为须要有梦想！还要有尽可能多的精神体验。'}
"""
# tokenizer is supported
tls.make_samples(text, jieba.lcut)
"""
{'delete': '人为什么活着？生而为人要有梦想！还要有尽可能多的精神体验。',
 'swap': '为什么人活着？生而为人必须要有梦想！还要有尽可能多的精神体验。',
 'insert': '人为什么活着？生而为人必须要有梦想！还要还要有尽可能多的精神体验。',
 'together': '人为什么活着？生而为人人要有梦想！还要有多尽可能的精神体验。'}
"""
# SentenceLevel
from pnlp import SentenceLevelSampler
sls = SentenceLevelSampler()
sls.make_samples(text)
"""
{'delete': '生而为人必须要有梦想！还要有尽可能多的精神体验。',
 'swap': '人为什么活着？还要有尽可能多的精神体验。生而为人必须要有梦想！',
 'insert': '人为什么活着？还要有尽可能多的精神体验。生而为人必须要有梦想！生而为人必须要有梦想！',
 'together': '生而为人必须要有梦想！人为什么活着？人为什么活着？'}
"""
```

TokenLevelSampler Note:

- It uses a default tokenizer for Chinese (Chinese Char Tokenizer) and English (Simple Whitespace Tokenizer).
- The tokenizer could be anyone you like, but the output should be a list of tokens or a list of tuple pairs, each pair include a token and a part-of-speech.
- It uses `stopwords` as default sample words and function part-of-speech as default sample pos. This means we only sampling those tokens who are in the sample words or their pos are in the sample pos (if they just have a pos). You could customize them as you like.

### Normalization

```python
from pnlp import num_norm
num_norm.num2zh(1024) == "一千零二十四"
num_norm.num2zh(1024).to_money() == "壹仟零贰拾肆"
num_norm.zh2num("一千零二十四") == 1024
```

### StopWords

```python
from pnlp import StopWords, chinese_stopwords, english_stopwords

csw = StopWords("/path/to/custom/stopwords.txt")
csw.stopwords # a set of the custom stopwords

csw.zh == chinese_stopwords # Chineses stopwords
csw.en == english_stopwords # English stopwords
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

### Concurring

```python
import math
def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True

from pnlp import concurring
@concurring
def get_primes(lst):
    res = []
    for i in lst:
        if is_prime(i):
            res.append(i)
    return res
@concurrint(type="thread", max_workers=10)
def get_primes(lst):
    pass
```

`concurring` wrapper just make your original function concurring. 

## Test

Clone the repo run:

```bash
$ python -m pytest
```

## ChangeLog

### v0.3.7

Add concurring and batch generator

### v0.3.5

Add text enhancement.


### v0.3.3/4

Fix url link and picture  `Regex` pattern.

### v0.3.2

Fix `cut_part` for sentence ends with a white space and a full stop. 

### v0.3.1

Add `cut_part` to cut text to any parts by the given Regex Pattern; Add `combine_bucket` to combine any parts to buckets by the given threshold(length).

### v0.3.0

Update `cut_sentence`; Add `NumNorm`.

### v0.28-29

Update `cut_zhchar`.

### v0.27

Add `cut_zhchar`.

### v0.26

Add `read_csv`, remove `；` as a sentence cut standard.

### v0.25

Add `stop_words`. 

### v0.24

Fix `read_json`.

### v0.23

Fix `Text` default rule.

### v0.22

Make `Text` more convenient to use.

### v0.21

Add `cut_sentence` method.

### v0.20

Optimize several interface and make `Text` accept list of Regular Expression Patterns.



