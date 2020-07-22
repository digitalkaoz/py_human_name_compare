# Human Name Compare

![human_name_compare](https://github.com/digitalkaoz/py_human_name_compare/workflows/human_name_compare/badge.svg)
[![PyPI version](https://badge.fury.io/py/human-name-compare.svg)](https://badge.fury.io/py/human-name-compare)


the Problem:

Check if `Dr. Peter Müller` and `Peter K. Müller` and `Dr. med. Peter Karsten Müller` and `P. Müller` indicate if its the same person

There are gazillion tiny bits and pieces which makes this trivial task hard e.g.:

* "R. Schönthal" "Robert Schönthal" - the only have initials on one side
* "Erik Schönthal" "Robert Schönthal" - the firstname name doesnt match
* "Robert Erik Schönthal" "Robert Peter Schönthal" - the middle name doesnt match 
* "Robert-Erik Schönthal" "Robert Erik Schönthal" - we have an "-" in our firstnames
* "Robeert Schönthal" "Robert Schönthal" - the firstname has a typo
* "Robert Müller" "Robert Schönthal" - the lastname doesnt match
* "Herr Robert Müller" "Dr. med. Robert Schönthal" - we have some prefixes

and so on...

## Usage

### CLI

```shell script
$ hn-compare compare "Robert Schönthal" "Robert Schönthal"
```

### Python

```python
from human_name_compare import match_name

match_name("Robert Schönthal", "Robert Schönthal")
```

## Tests

````shell script
$ python -m pytest .
````