<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [功能特性](#%E5%8A%9F%E8%83%BD%E7%89%B9%E6%80%A7)
- [安装](#%E5%AE%89%E8%A3%85)
- [使用](#%E4%BD%BF%E7%94%A8)
  - [文本IO](#%E6%96%87%E6%9C%ACio)
    - [IO 处理](#io-%E5%A4%84%E7%90%86)
    - [内置方法](#%E5%86%85%E7%BD%AE%E6%96%B9%E6%B3%95)
  - [文本处理](#%E6%96%87%E6%9C%AC%E5%A4%84%E7%90%86)
    - [清理和提取](#%E6%B8%85%E7%90%86%E5%92%8C%E6%8F%90%E5%8F%96)
    - [内置正则](#%E5%86%85%E7%BD%AE%E6%AD%A3%E5%88%99)
  - [文本切分](#%E6%96%87%E6%9C%AC%E5%88%87%E5%88%86)
    - [任意部分切分](#%E4%BB%BB%E6%84%8F%E9%83%A8%E5%88%86%E5%88%87%E5%88%86)
    - [分句](#%E5%88%86%E5%8F%A5)
    - [中文字符切分](#%E4%B8%AD%E6%96%87%E5%AD%97%E7%AC%A6%E5%88%87%E5%88%86)
    - [句子分组](#%E5%8F%A5%E5%AD%90%E5%88%86%E7%BB%84)
  - [文本增强](#%E6%96%87%E6%9C%AC%E5%A2%9E%E5%BC%BA)
    - [Token级别](#token%E7%BA%A7%E5%88%AB)
    - [句子级别](#%E5%8F%A5%E5%AD%90%E7%BA%A7%E5%88%AB)
  - [文本归一化](#%E6%96%87%E6%9C%AC%E5%BD%92%E4%B8%80%E5%8C%96)
    - [中文数字](#%E4%B8%AD%E6%96%87%E6%95%B0%E5%AD%97)
  - [格式转换](#%E6%A0%BC%E5%BC%8F%E8%BD%AC%E6%8D%A2)
    - [BIO转实体](#bio%E8%BD%AC%E5%AE%9E%E4%BD%93)
  - [内置词典](#%E5%86%85%E7%BD%AE%E8%AF%8D%E5%85%B8)
    - [停用词](#%E5%81%9C%E7%94%A8%E8%AF%8D)
  - [文本长度](#%E6%96%87%E6%9C%AC%E9%95%BF%E5%BA%A6)
  - [魔术方法](#%E9%AD%94%E6%9C%AF%E6%96%B9%E6%B3%95)
  - [并行处理](#%E5%B9%B6%E8%A1%8C%E5%A4%84%E7%90%86)
- [测试](#%E6%B5%8B%E8%AF%95)
- [更新日志](#%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

NLP 预/后处理工具。

## 功能特性

- 专为文本 IO 设计的灵活的 Pipeline
- 灵活的文本清理/提取工具
- 文本增强
- 按句切分或按中文字符切分文本
- 文本分桶
- 中文字符归一化
- 文本各种长度计算
- 中英文常用停用词
- 预处理魔术方法
- 并发、批量化、实体 BIO 转实体

## 安装

需要 Python3.7+。

`pip install pnlp`

## 使用

### 文本IO

#### IO 处理

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
pattern = '*.md' # 可以是 '*.txt', 'f*.*' 等，支持正则
reader = Reader(pattern, use_regex=True)

# 获取所有文件的行，输出行文本、行索引和所在的文件名
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

# 获取某个文件的所有行，输出行文本、行索引和所在文件名，此时由于指定了文件名 pattern 无效
for line in reader(os.path.join(DATA_FOLDER_PATH, "a.md")):
    print(line.lid, line.fname, line.text)
"""
0 a.md line 1 in a.
1 a.md line 2 in a.
2 a.md line 3 in a.
"""



# 获取目录下的所有文件路径
for path in Reader.gen_files(DATA_PATH, pattern, use_regex: True):
    print(path)
"""
pnlp/tests/piop_data/a.md
pnlp/tests/piop_data/first/fa.md
pnlp/tests/piop_data/first/second/sa.md
"""

# 获取一个目录下所有文件名和它们的内容
paths = Reader.gen_files(DATA_PATH, pattern)
articles = Reader.gen_articles(paths)
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

# 同前两个例子
paths = Reader.gen_files(DATA_PATH, pattern)
articles = Reader.gen_articles(paths)
for line in Reader.gen_flines(articles, strip="\n"):
    print(line.lid, line.fname, line.text)
```

#### 内置方法

```python
import pnlp

# Read
file_string = pnlp.read_file(file_path)
file_list = pnlp.read_lines(file_path)
file_json = pnlp.read_json(file_path)
file_yaml = pnlp.read_yaml(file_path)
file_csv = pnlp.read_csv(file_path)
file_pickle = pnlp.read_pickle(file_path)
list_dict = pnlp.read_file_to_list_dict(file_path)

# Write
pnlp.write_json(file_path, data, indent=2)
pnlp.write_file(file_path, data)
pnlp.write_pickle(file_path, data)
pnlp.write_list_dict_to_file(file_path, data)

# Others
pnlp.check_dir(dirname) # 如果目录不存在会创建
```

### 文本处理

#### 清理和提取

```python
import re
from pnlp import Text

text = "这是https://www.yam.gift长度测试，《 》*)FSJfdsjf😁![](http://xx.jpg)。233."
pattern = re.compile(r'\d+')

# pattern 是 re.Pattern 类型或 str 类型
# 默认为空字符串：'', 表示不使用任何 pattern（实际是 re.compile(r'.+')），此时 clean 返回空（全部被清了），extract 返回原始文本。
# pattern 支持以下字符串类型（实际为正则）：
#	'chi': 中文字符
#	'pun': 标点
#	'whi': 空白
#	'nwh': 非空白
#	'wnb': 字母（含中文字符）或数字
#	'nwn': 非字母（含中文字符）或数字
#	'eng': 英文字符
#	'num': 数字
#	'pic': 图片
#	'lnk': 链接
#	'emj': 表情

pt = Text(['chi', pattern])

# 提取所有符合 pattern 的文本和它们的位置
res = pt.extract(text)
print(res)
"""
{'text': '这是长度测试233', 'mats': ['这是', '长度测试', '233'], 'locs': [(0, 2), (22, 26), (60, 63)]}
"""
# 支持用「点」获取key属性
print(res.text, res.mats, res.locs)
"""
'这是长度测试' ['这是', '长度测试'] [(0, 2), (22, 26)]
"""

# 返回指定 pattern 清理后的文本
print(pt.clean(text))
"""
https://www.yam.gift，《 》*)FSJfdsjf😁![](http://xx.jpg)。233.
"""

# 可以指定多个 pattern，注意先后顺序可能会影响结果哦
pt = Text(['pic', 'lnk'])
# 提取到的
res = pt.extract(text)
print(res.mats)
"""
['https://www.yam.gif',
 '![](http://xx.jpg)',
 'https://www.yam.gift',
 'http://xx.jpg']
"""
# 清理后的
print(pt.clean(text))
"""
这是t长度测试，《 》*)FSJfdsjf😁。233.
"""
```

#### 内置正则

```python
# USE Regex
from pnlp import reg
def clean_text(text: str) -> str:
    text = reg.pwhi.sub("", text)
    text = reg.pemj.sub("", text)
    text = reg.ppic.sub("", text)
    text = reg.plnk.sub("", text)
    return text
```

### 文本切分

#### 任意部分切分

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

#### 分句

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

#### 中文字符切分

```python
# 中文字符切分
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

#### 句子分组

```python
from pnlp import combine_bucket
parts = [
    "先生，那夜，我因胸中纳闷，无法入睡，",
    "折腾得比那铐了脚镣的叛变水手还更难过；",
    "那时，我就冲动的 ——",
    "好在有那一时之念，",
    "因为有时我们在无意中所做的事能够圆满……"
]
buckets = combine_bucket(parts.copy(), 10, truncate=True, keep_remain=True)
print(buckets)
"""
['先生，那夜，我因胸中',
 '纳闷，无法入睡，',
 '折腾得比那铐了脚镣的',
 '叛变水手还更难过；',
 '那时，我就冲动的 —',
 '—',
 '好在有那一时之念，',
 '因为有时我们在无意中',
 '所做的事能够圆满……']
"""
```

### 文本增强

采样器支持删除、交换、插入操作，所有的操作不会跨越标点。

#### Token级别

- 默认 Tokenizer
    - 中文：字符级 Tokenizer（见上）
    - 英文：空白符切分 Tokenizer
- Tokenizer 可以任意指定，但它的输出应该是一个 List 的 Token 或一个 List 的 Tuple，每个 Tuple 包含一个 Token 和一个词性。
- 对字符级增强，默认并不会操作所有字或词。可以自定义要操作的词或词性。
    - 默认 Token 是「停用词」
    - 默认词性（当 Tokenizer 输出带词性时）是「功能词」：副词、介词、连词、助词、其他虚词（标记为 d p c u xc）

```python
# 【】内的为改变的
text = "人为什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。"
# 字符粒度
from pnlp import TokenLevelSampler
tls = TokenLevelSampler()
tls.make_samples(text)
"""
{'delete': '人为什么活着？生而为人必须要【有】梦想！还要有尽可能多的精神体验。',
 'swap': '【为】【人】什么活着？生而为人必须要有梦想！还要有尽可能多的精神体验。',
 'insert': '人为什么活着？生而为人必须要有梦想！【还】还要有尽可能多的精神体验。',
 'together': '人什么着着活？生而必为为须要有梦想！还要有尽可能多的精神体验。'}
"""
# 支持自定义 tokenizer
tls.make_samples(text, jieba.lcut)
"""
{'delete': '人为什么活着？生而为人【必须】要有梦想！还要有尽可能多的精神体验。',
 'swap': '【为什么】【人】活着？生而为人必须要有梦想！还要有尽可能多的精神体验。',
 'insert': '人为什么活着？生而为人必须要有梦想！【还要】还要有尽可能多的精神体验。',
 'together': '人为什么活着？生而为人人要有梦想！还要有多尽可能的精神体验。'}
"""
# 自定义
tls = TokenLevelSampler(
    rate=替换比例, # 默认 5%
    types=["delete", "swap", "insert"], # 默认三个 
    sample_words=["词1", "词2"], # 默认停用词
    sample_pos=["词性1", "词性2"], # 默认功能词
)
```

#### 句子级别

```python
from pnlp import SentenceLevelSampler
sls = SentenceLevelSampler()
sls.make_samples(text)
"""
{'delete': '生而为人必须要有梦想！还要有尽可能多的精神体验。',
 'swap': '人为什么活着？还要有尽可能多的精神体验。生而为人必须要有梦想！',
 'insert': '人为什么活着？还要有尽可能多的精神体验。生而为人必须要有梦想！生而为人必须要有梦想！',
 'together': '生而为人必须要有梦想！人为什么活着？人为什么活着？'}
"""
# 自定义
sls = SentenceLevelSampler(types=["delete", "swap", "insert"]) # 默认三个
```

### 文本归一化

#### 中文数字

```python
from pnlp import num_norm
num_norm.num2zh(1024) == "一千零二十四"
num_norm.num2zh(1024).to_money() == "壹仟零贰拾肆"
num_norm.zh2num("一千零二十四") == 1024
```

### 格式转换

#### BIO转实体

```python
# 实体 BIO Token 转实体
from pnlp import pick_entity_from_bio_labels
pairs = [('天', 'B-LOC'), ('安', 'I-LOC'), ('门', 'I-LOC'), ('有', 'O'), ('毛', 'B-PER'), ('主', 'I-PER'), ('席', 'I-PER')]
pick_entity_from_bio_labels(pairs)
"""
[('天安门', 'LOC'), ('毛主席', 'PER')]
"""
pick_entity_from_bio_labels(pairs, with_offset=True)
"""
[('天安门', 'LOC', 0, 3), ('毛主席', 'PER', 4, 7)]
"""
```

#### 任意参数转UUID

```python
from pnlp import generate_uuid

uid1 = pnlp.generate_uuid("a", 1, 0.02)
uid2 = pnlp.generete_uuid("a", 1)
"""
uid1 == 3fbc8b70d05b5abdb5badca1d26e1dbd
uid2 == f7b0ffc589e453e88d4faf66eb92f669
"""
```

### 内置词典

#### 停用词

```python
from pnlp import StopWords, chinese_stopwords, english_stopwords

csw = StopWords("/path/to/custom/stopwords.txt")
csw.stopwords # a set of the custom stopwords

csw.zh == chinese_stopwords # Chineses stopwords
csw.en == english_stopwords # English stopwords
```


### 文本长度

```python
from pnlp import Length

text = "这是https://www.yam.gift长度测试，《 》*)FSJfdsjf😁![](http://xx.jpg)。233."

pl = Length(text)
# 注意：即使使用了 pattern，长度都是基于原始文本
# 长度基于字符计数（不是整词）
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

### 魔术方法

```python
from pnlp import MagicDict

# 嵌套字典
pmd = MagicDict()
pmd['a']['b']['c'] = 2
print(pmd)

"""
{'a': {'b': {'c': 2}}}
"""

# 当字典被翻转时，保留所有的重复 value-keys
dx = {1: 'a',
      2: 'a',
      3: 'a',
      4: 'b' }
print(pmag.MagicDict.reverse(dx))

"""
{'a': [1, 2, 3], 'b': 4}
"""
```

### 并行处理

支持四种并行处理方式：

- 线程池：`thread_pool`
- 进程池：`process_pool`
- 线程 Executor：`thread_executor`，默认使用
- 线程：`thread`

注意：惰性处理，返回的是 Generator。

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

# max_workers 默认为 4
@concurring
def get_primes(lst):
    res = []
    for i in lst:
        if is_prime(i):
            res.append(i)
    return res

@concurrint(type="thread_pool", max_workers=10)
def get_primes(lst):
    pass
```

`concurring` 装饰器让你的迭代函数并行。

## 测试

Clone 仓库后执行：

```bash
$ python -m pytest
```

## 更新日志

见英文版 README。



