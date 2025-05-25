@echo off

REM Create virtual environment
python -m venv xenv

REM Activate virtual environment
call xenv\Scripts\activate.bat

REM Install packages
pip install magika
pip install colorama
pip install pyinstaller

REM Build executable
pyinstaller --collect-all magika --onefile spell.py

REM Copy executable to current directory
copy dist\spell.exe spell.exe

REM Clean up files and folders
del spell.spec
rmdir /s /q dist
rmdir /s /q build
rmdir /s /q xenv
