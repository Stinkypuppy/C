import subprocess
import sys
from pathlib import Path
import os

# Dynamic dependency installation
required_packages = ["rich", "pyfiglet", "questionary", "tqdm", "alive-progress", "tkinter", "colorama", "termcolor", "curses", "art", "asciimatics"]
subprocess.check_call([sys.executable, "-m", "pip", "install"] + required_packages)

import questionary
from tqdm import tqdm
from pyfiglet import Figlet
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from alive_progress import alive_bar
from art import *
from asciimatics.screen import Screen
from termcolor import colored
from colorama import Fore, Back, Style
import curses

console = Console()

def custom_title_screen(screen):
    screen.clear()
    fig = Figlet(font='starwars')
    title = fig.renderText('File Split Tool by Guinness')
    for line in title.split('\n'):
        screen.print_at(line, 0, screen.height // 2 - 4 + title.split('\n').index(line), colour=Screen.COLOUR_MAGENTA)
        screen.refresh()
        curses.napms(100)
    screen.wait_for_input(10)

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

def split_file(filename, size):
    size = int(size) * 1024 * 1024  # Convert size to bytes
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

def join_files(base_filename, num_parts):
    with Progress(SpinnerColumn(), BarColumn(), TextColumn("[progress.description]{task.description}"), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), console=console) as progress:
        task = progress.add_task("[cyan]Joining files...", total=num_parts)
        with open(f"{base_filename}_joined", 'wb') as dst:
            for i in range(1, num_parts + 1):
                with open(f"{base_filename}.part{i}", 'rb') as src:
                    data = src.read()
                    dst.write(data)
                    progress.advance(task)
    console.print("[bold green]Files have been successfully joined.[/bold green]")

def main():
    Screen.wrapper(custom_title_screen)
    console.print(Markdown("# 🌌 [blink]File Split and Join Tool [/blink] 🌌"))
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
        base_filename = questionary.text("Enter the base filename (without .partN):").ask()
        num_parts = int(questionary.text("How many parts are there?").ask())
        join_files(base_filename, num_parts)

if __name__ == "__main__":
    main()
