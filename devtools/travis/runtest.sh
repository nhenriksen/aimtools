#!/bin/sh
set -ex

echo "Simplest possible testing regimen"
cd aimtools/tests

coverage pytest test_unique_types.py
