#!/bin/sh
set -ex

echo "Simplest possible testing regimen"
cd aimtools/tests

#source activate myenv

#echo 'AFTER'
which python
python --version
which pytest
pytest --version
which parmed
parmed --version

pytest test_unique_types.py

