# Human Name Compare

the Problem:

check if `Dr. Peter Müller` and `Peter K. Müller` and `Dr. med. Peter Karsten Müller` and `P. Müller` indicate if its the same person

## Usage

### CLI

```shell script
$ hn-compare compare "Robert Schönthal" "Robert Schönthal"
```

### Python

```python
from hn_compare import match_name

match_name("Robert Schönthal", "Robert Schönthal")
```

## Tests

````shell script
$ python -m pytest .
````