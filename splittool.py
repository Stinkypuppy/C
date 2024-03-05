import os
import subprocess
import sys
from pathlib import Path

# Auto-install dependencies
def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "questionary", "tqdm", "pyfiglet"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        sys.exit(1)

install_dependencies()

import questionary
from tqdm import tqdm
from pyfiglet import Figlet

def split_file(filename, size):
    size = int(size) * 1024 * 1024  # Convert size to bytes
    part_num = 0
    with open(filename, 'rb') as src:
        chunk = src.read(size)
        pbar = tqdm(total=os.path.getsize(filename), unit='B', unit_scale=True, desc="Splitting file")
        while chunk:
            part_num += 1
            with open(f"{filename}.part{part_num}", 'wb') as dst:
                dst.write(chunk)
                pbar.update(len(chunk))
            chunk = src.read(size)
        pbar.close()
    print(f"File split into {part_num} parts.")

def join_files(base_filename, num_parts):
    with open(f"{base_filename}_joined", 'wb') as dst:
        for i in range(1, num_parts + 1):
            with open(f"{base_filename}.part{i}", 'rb') as src:
                data = src.read()
                pbar = tqdm(total=len(data), unit='B', unit_scale=True, desc=f"Joining part {i}")
                dst.write(data)
                pbar.update(len(data))
                pbar.close()
    print("Files have been successfully joined.")

def main():
    f = Figlet(font='slant')
    print(f.renderText('File Splitter & Joiner'))

    action = questionary.select(
        "Choose an action:",
        choices=["Split a file", "Join files"],
    ).ask()

    if action == "Split a file":
        filename = questionary.text("Enter the filename:").ask()
        size = questionary.text("Enter the size of each part (in MB):").ask()
        split_file(filename, size)
    elif action == "Join files":
        base_filename = questionary.text("Enter the base filename (without .partN):").ask()
        num_parts = int(questionary.text("How many parts are there?").ask())
        join_files(base_filename, num_parts)

if __name__ == "__main__":
    main()
