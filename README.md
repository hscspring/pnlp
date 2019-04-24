# pnlp
This is a pre-processing tool for NLP.

## Install

`pip install pnlp`

## Usage Examples

### iopipe

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

### text

