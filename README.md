# Recursive File Type detector based on Google Magika


## Features

- Displays directory structure up to a configurable depth.
- Identifies and predicts file types with Google Magika.
- Colors file types dynamically for easier readability.
- Verbose mode to show prediction accuracy, MIME types, and extensions.

---

## Installation

Clone the repository and run the install script:

   ```bash
   git clone https://github.com/catalincd/Spell
   cd Spell
   ./install.sh
   ```

## Run the spell
```bash
   ./spell /home/wizard --verbose --level 3
   ./spell . -v -l 3
   ```

## More help
```
   > ./spell --help
   usage: spell [-h] [-v] [-l LEVEL] path

	Tree with file extensions using Google Magika

	positional arguments:
	  path               Path to a file or directory

	options:
	  -h, --help         show this help message and exit
	  -v, --verbose      Enable verbose output
	  -l, --level LEVEL  Maximum depth level (5 by default)
```

![image](https://github.com/user-attachments/assets/46a28e22-2abc-47f6-9e8d-c19133273d95)
