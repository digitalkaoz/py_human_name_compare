#!/usr/bin/env bash

rm -rf dist
python setup.py dist
twine upload dist/*