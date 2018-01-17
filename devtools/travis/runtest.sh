#!/bin/sh
set -ex

echo "Simplest possible testing regimen"
cd aimtools/tests
which pytest
pytest --version
pytest test_unique_types.py

