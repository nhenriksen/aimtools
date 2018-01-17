#!/bin/sh
set -ex

echo "Simplest possible testing regimen"
cd aimtools/test
pytest test_unique_types.py

