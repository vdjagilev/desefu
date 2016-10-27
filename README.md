Desefu
======
[![Build Status](https://travis-ci.org/vdjagilev/desefu.svg?branch=master)](https://travis-ci.org/vdjagilev/desefu)
[![Coverage Status](https://coveralls.io/repos/github/vdjagilev/desefu/badge.svg?branch=master)](https://coveralls.io/github/vdjagilev/desefu?branch=master)
[![Code Climate](https://codeclimate.com/github/vdjagilev/desefu/badges/gpa.svg)](https://codeclimate.com/github/vdjagilev/desefu)

Digital evidence search-extract forensic utility.
Used to narrow digital evidence search process and extract found data.

# Installation and Requirements

In order to make it run a recent version of Python is required (at least 3.4)

```
# pip install -r requirements.txt
```

# Usage

```
./desefu.py ~/path/to/config.yml ~/path/to/evidence/folder
```

# Config file

An example of config file:
```yml
author: Name Surname
search:
  seach_id_1: # Module chain ID
    -
      mod: file.Extension # This module filter files by their extension
      args: ['doc', 'docx', 'xls', 'xlsx']
    -
      mod: some.Module
      args: ['arguments', 'for', 'each', 'module', 'are', 'unique']
      sub: # Another (sub)module chain
        -
          mod: some.other.Module
          extract: # Optional parameter, not all modules support this
            abc: 123
  search_jpg: # For each module chain, initial list of files is the same
    -
      mod: file.Extension
      args: ['', 'jpg', 'jpeg']
    -
      mod: file.FileHeader
      args:
        - [FF, D8, FF, E0, 00, 10, 4A, 46, 49, 46]
    -
      mod: file.type.jpeg.Exif
      extract:
        gps: true
        model: true
```
