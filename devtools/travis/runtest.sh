#!/bin/sh
set -ex

echo "Simplest possible testing regimen"
cd aimtools/tests

pytest test_unique_types.py
