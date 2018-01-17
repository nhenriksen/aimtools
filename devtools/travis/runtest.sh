#!/bin/sh
set -ex

echo "Simplest possible testing regimen"
cd aimtools/tests

echo 'BEFORE'
which python
python --version
which pytest
pytest --version

source activate myenv

echo 'AFTER'
which python
python --version
which pytest
pytest --version


pytest test_unique_types.py

