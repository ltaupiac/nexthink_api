# pylint: skip-file
# ruff: noqa

from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty

console = Console()


def step(message: str) -> None:
    console.print(f"\n[bold cyan]{message}[/bold cyan]")


def info(message: str) -> None:
    console.print(f"[bold cyan]{message}[/bold cyan]")


def ok(message: str) -> None:
    console.print(f"[bold green]OK[/bold green] {message}")


def ko(message: str) -> None:
    console.print(f"[bold red]KO[/bold red] {message}")


def panel(value, title: str, border_style: str = "green") -> None:
    console.print(Panel(Pretty(value), title=title, border_style=border_style))


def text_panel(value: str, title: str, border_style: str = "green") -> None:
    console.print(Panel(value, title=title, border_style=border_style))
