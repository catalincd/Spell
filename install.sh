#!/bin/bash

python -m venv xenv
source xenv/bin/activate

pip install magika
pip install colorama
pip install pyinstaller

pyinstaller --collect-all magika --onefile spell.py
cp dist/spell ./spell

rm spell.spec
rm -rf dist
rm -rf build
rm -rf xenv