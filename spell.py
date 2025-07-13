from magika import Magika
import os
import argparse
import shutil
from pathlib import Path
import random
from colorama import init, Fore, Style
import platform
import subprocess

parser = argparse.ArgumentParser(description="Tree with file extensions using Google Magika")
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('-l', '--level', type=int, help='Maximum depth level (5 by default)')
parser.add_argument('path', type=Path, help='Path to a file or directory')
parser.add_argument('-t', '--trid', action='store_true', help='Enable TrID')
parser.add_argument('-p' , '--trid-path', default=('trid.exe' if platform.system() == "Windows" else 'trid'), help='Path to TrID binary')

args = parser.parse_args()

init(autoreset=True)
magika = Magika()
max_level = args.level if args.level else 5
trid_path = args.trid_path if args.trid_path else "loco"

color_values = [value for name, value in vars(Fore).items() if not name.startswith("_")]
random.shuffle(color_values)
dynamic = {}

def get_color(file_type):
    global color_values
    global dynamic
    
    if file_type not in dynamic:
        dynamic[file_type] = color_values[0]
        color_values.pop(0)

        if len(color_values) < 5:
            color_values = [value for name, value in vars(Fore).items() if not name.startswith("_")]
            random.shuffle(color_values)
    
    return dynamic[file_type]
        
def print_file_trid(prefix, pointer, name, path, name_len):
    global args
    result = subprocess.run([trid_path, os.path.abspath(path)], capture_output=True, text=True).stdout
    result = result.replace("TrID is best suited to analyze binary files!", "")
    result = result.replace("file seems to be ", "")
    result = result.replace("Warning:", "")
    trim = lambda line: " ".join(line.split()[:4])
    formatted = " ".join(map(trim, result.splitlines()[6:10]))

    padding = ' ' * (min(50, (5 + name_len - len(name))))
    print(f'{prefix}{pointer}{path}{padding}{formatted}')


def print_file(prefix, pointer, name, path, name_len):
    global args
    result = magika.identify_path(path)
    predicted = result.prediction.output.description
    acc = f'{Style.RESET_ALL}{int(result.prediction.score * 100.0)}%' if args.verbose else ''
    ext = f'{Style.BRIGHT}{' / '.join(result.prediction.output.extensions)}' if args.verbose else ''
    mime = f'{Style.RESET_ALL}{result.prediction.output.mime_type}' if args.verbose else ''
    if predicted == 'A directory':
        print(f'{prefix}{pointer}{Style.BRIGHT}{name}')
    else:
        padding = ' ' * (min(50, (5 + name_len - len(name))))
        padding_right = ' ' * max(0, (32 - len(predicted)))
        padding_mime = ' ' * max(0, (20 - len(ext)))
        print(f'{prefix}{pointer}{name}{padding}{Style.BRIGHT}{get_color(result.prediction.output.description)}{predicted}{padding_right}{acc} {ext}{padding_mime}{mime}')

def tree(directory, prefix='', level=0):
    if level == max_level:
        return

    entries = os.listdir(directory)   
    dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
    files = [e for e in entries if not os.path.isdir(os.path.join(directory, e))]
    dirs.sort()
    files.sort()
    contents = dirs + files
    pointers = ['├── '] * (len(contents) - 1) + ['└── ']
    
    name_len = max(len(s) for s in contents) if len(contents) > 0 else 0

    for pointer, name in zip(pointers, contents):
        path = os.path.join(directory, name)
        if args.trid:
            print_file_trid(prefix, pointer, name, path, name_len)
        else:
            print_file(prefix, pointer, name, path, name_len)

        if os.path.isdir(path):
            extension = '│   ' if pointer == '├── ' else '     '
            tree(path, prefix + extension, level+1)


if __name__ == "__main__":
    directory = args.path
    print(trid_path)
    print(directory)
    tree(directory)
