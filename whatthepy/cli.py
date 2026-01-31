import os
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn
from rich.prompt import Prompt
import pyfiglet

from whatthepy.obfuscator import obfuscate

console = Console()

def main():
    banner = pyfiglet.figlet_format("WhatThePy", font="slant")
    console.print(banner, style="bold cyan")
    console.print("[dim]Compress -> Encrypt -> Scatter[/dim]\n")

    while True:
        filepath = Prompt.ask("[cyan]File path[/cyan]")
        filepath = filepath.strip().strip('"').strip("'")

        if not filepath:
            console.print("[red]Enter a file path[/red]")
            continue

        if not os.path.exists(filepath):
            console.print(f"[red]Not found: {filepath}[/red]")
            continue

        if not filepath.endswith('.py'):
            console.print("[red]Must be a .py file[/red]")
            continue

        break

    size = Path(filepath).stat().st_size
    size_str = f"{size} B" if size < 1024 else f"{size/1024:.1f} KB"
    console.print(f"[dim]→[/dim] {filepath} [dim]({size_str})[/dim]\n")

    p = Path(filepath)
    output = p.parent / f"{p.stem}_obfuscated.py"

    with Progress(
        BarColumn(bar_width=40),
        "[cyan]{task.description}",
        console=console
    ) as progress:
        task = progress.add_task("", total=100)

        def on_progress(pct, msg):
            progress.update(task, completed=pct, description=msg)

        try:
            stats = obfuscate(filepath, str(output), on_progress)
        except SyntaxError as e:
            console.print(f"\n[red]Syntax error: {e}[/red]")
            sys.exit(1)

    console.print()
    console.print(f"[green]✓[/green] Saved to [cyan]{output}[/cyan]")

    orig_size = stats['original_size']
    final_size = stats['final_size']
    orig_str = f"{orig_size} B" if orig_size < 1024 else f"{orig_size/1024:.1f} KB"
    final_str = f"{final_size} B" if final_size < 1024 else f"{final_size/1024:.1f} KB"

    console.print(f"[dim]  {orig_str} → {final_str} | {stats['chunks']} chunks | {stats['decoys']} decoys[/dim]")
    console.print(f"\n[dim]pyinstaller --onefile {output}[/dim]")

if __name__ == "__main__":
    main()
