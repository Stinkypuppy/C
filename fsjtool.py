import subprocess
import sys
from pathlib import Path
import os

# Removed 'curses' from required_packages since it's not available for newer Python versions and not directly installable via pip
required_packages = ["rich", "pyfiglet", "questionary", "tqdm", "alive-progress", "PyQt6", "colorama", "termcolor", "art", "asciimatics"]
subprocess.check_call([sys.executable, "-m", "pip", "install"] + required_packages)

import questionary
from tqdm import tqdm
from pyfiglet import Figlet
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from alive_progress import alive_bar
from art import *
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer
from termcolor import colored
from colorama import Fore, Back, Style

console = Console()

class CustomTitleScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('File Split Tool by Guinness')
        layout = QVBoxLayout()

        fig = Figlet(font='starwars')
        title = fig.renderText('File Split Tool by Guinness')
        label = QLabel(title)
        layout.addWidget(label)

        self.setLayout(layout)
        # Close automatically after a certain time
        QTimer.singleShot(5000, self.close) # 5000 milliseconds = 5 seconds

def install_dependencies():
    console.print("[bold cyan]Ensuring all dependencies are up-to-date...[/bold cyan]", style="bold cyan")
    try:
        for package in required_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        console.print("[bold green]All dependencies are installed![/bold green]", style="bold green")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Failed to install dependencies: {e}[/bold red]", style="bold red")
        sys.exit(1)

install_dependencies()

def detect_split_files(directory):
    files = Path(directory).glob('*.part*')
    base_filenames = set()
    for file in files:
        base_name = ".".join(str(file).split('.')[:-1])
        base_filenames.add(base_name)
    return list(base_filenames)

def split_file(filename, size):
    size = int(size) * 1024 * 1024
    part_num = 0
    with open(filename, 'rb') as src:
        chunk = src.read(size)
        with Progress(SpinnerColumn(), BarColumn(), TextColumn("[progress.description]{task.description}"), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), console=console) as progress:
            total_size = os.path.getsize(filename)
            task = progress.add_task("[cyan]Splitting file...", total=total_size)
            while chunk:
                part_num += 1
                with open(f"{filename}.part{part_num}", 'wb') as dst:
                    dst.write(chunk)
                    progress.update(task, advance=len(chunk))
                chunk = src.read(size)
    console.print(f"[bold magenta]File split into {part_num} parts.[/bold magenta]")

def join_files(base_filename):
    parts = sorted(Path('.').glob(f'{base_filename}.part*'), key=lambda x: int(x.suffix.split('part')[1]))
    num_parts = len(parts)
    if num_parts == 0:
        console.print("[bold red]No split files provided.[/bold red]")
        return

    with Progress(SpinnerColumn(), BarColumn(), TextColumn("[progress.description]{task.description}"), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), console=console) as progress:
        task = progress.add_task("[cyan]Joining files...", total=num_parts)
        with open(f"{base_filename}_joined", 'wb') as dst:
            for part in parts:
                with open(part, 'rb') as src:
                    data = src.read()
                    dst.write(data)
                    progress.advance(task)
    console.print("[bold green]Files have been successfully joined.[/bold green]")

def main():
    app = QApplication(sys.argv)
    ex = CustomTitleScreen()
    ex.show()
    app.exec()

    console.print(Markdown("# [blink]File Split and Join Tool [/blink] "))
    console.print(Markdown("### [italic magenta]Made and Designed by Guinness Shepherd[/italic magenta]"))

    action = questionary.select(
        "Choose an action:",
        choices=["Split a file", "Join files"],
    ).ask()

    if action == "Split a file":
        filename = questionary.text("Enter the path of the file to be split:").ask()
        size = questionary.text("Enter the size of each part (in MB):").ask()
        split_file(filename, size)
    elif action == "Join files":
        detected_files = detect_split_files('.')
        base_filename = questionary.select("Select the base filename to join:", choices=detected_files).ask()
        join_files(base_filename)

if __name__ == "__main__":
    main()
