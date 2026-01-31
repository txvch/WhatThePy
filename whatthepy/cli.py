import os
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn
from rich.prompt import Prompt
import pyfiglet
from whatthepy.obfuscator import obfuscate

console = Console()

def fmt_size(n):
    return f"{n} B" if n < 1024 else f"{n/1024:.1f} KB"

def get_file():
    while True:
        path = Prompt.ask("[cyan]File path[/cyan]").strip().strip('"\'')

        if not path:
            console.print("[red]Enter a file path[/red]")
            continue

        if not os.path.exists(path):
            console.print(f"[red]Not found: {path}[/red]")
            continue

        if not path.endswith('.py'):
            console.print("[red]Must be a .py file[/red]")
            continue

        return path

def main():
    banner = pyfiglet.figlet_format("WhatThePy", font="slant")
    console.print(banner, style="bold cyan")
    console.print("[dim]Compress -> Encrypt -> Scatter[/dim]\n")

    path = get_file()
    size = Path(path).stat().st_size
    console.print(f"[dim]→[/dim] {path} [dim]({fmt_size(size)})[/dim]\n")

    p = Path(path)
    output = p.parent / f"{p.stem}_obfuscated.py"

    with Progress(BarColumn(bar_width=40), "[cyan]{task.description}", console=console) as prog:
        task = prog.add_task("", total=100)

        def on_progress(pct, msg):
            prog.update(task, completed=pct, description=msg)

        try:
            stats = obfuscate(path, str(output), on_progress)
        except SyntaxError as e:
            console.print(f"\n[red]Syntax error: {e}[/red]")
            sys.exit(1)

    console.print()
    console.print(f"[green]✓[/green] Saved to [cyan]{output}[/cyan]")
    console.print(f"[dim]  {fmt_size(stats['original_size'])} → {fmt_size(stats['final_size'])} | {stats['chunks']} chunks | {stats['decoys']} decoys[/dim]")
    console.print(f"\n[dim]pyinstaller --onefile {output}[/dim]")

if __name__ == "__main__":
    main()
