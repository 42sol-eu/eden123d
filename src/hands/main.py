"""Unified CLI that can run with pytest/behave/robot and produce Robot XML."""
from __future__ import annotations

import logging  # https://docs.python.org/3/library/logging.html
import sys  # https://docs.python.org/3/library/sys.html
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html
from typing import List  # https://docs.python.org/3/library/typing.html

import typer  # https://typer.tiangolo.com/
from rich.console import Console  # https://rich.readthedocs.io/

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.INFO, format=S_LOG_MSG_FORMAT)
log = logging.getLogger(__name__)
console = Console()
app = typer.Typer(help="Unified test runner that can emit Robot-style output.xml")


def _exit(rc: int) -> None:
    """Exit helper to keep cyclomatic complexity low."""
    quote = "Don't Panic — but bring a towel. (Douglas Adams)"
    if rc == 0:
        log.info(quote)
    else:
        log.info("So long, and thanks for all the fish. RC=%s", rc)
    raise typer.Exit(code=rc)


@app.command()
def run(
    engine: str = typer.Option("pytest", "--engine", "-e",
                               help="pytest | robot | behave"),
    args: List[str] = typer.Argument(None, help="Arguments passed to the engine"),
) -> None:
    """Run tests with the chosen engine, forwarding arguments."""
    # No regex here; passing args through untouched
    log.debug("run(engine=%s, args=%s)", engine, args)
    rc = 1
    try:
        if engine == "pytest":
            import pytest  # https://docs.pytest.org/
            # Ensure plugin is active (it is via entry point). User can override output with --robot-output
            rc = pytest.main(list(args))
        elif engine == "behave":
            from behave.__main__ import main as behave_main  # https://behave.readthedocs.io/
            # Suggest: -f robotxml -o output.xml to generate Robot XML
            rc = behave_main(list(args))
        elif engine == "robot":
            from robot import run_cli  # https://robot-framework.readthedocs.io/en/stable/autodoc/robot.html
            rc = run_cli(list(args), exit=False)
        else:
            console.print(f"[bold red]Unknown engine: {engine}[/bold red]")
            rc = 2
    except Exception as exc:  # noqa: BLE001
        log.error("Engine failed: %s", exc)
        rc = 3
    _exit(rc)


@app.command()
def rebot(args: List[str] = typer.Argument(None, help="Args to pass to rebot")) -> None:
    """Pass-through to Robot's rebot for HTML reports from any Robot-XML."""
    log.debug("rebot(args=%s)", args)
    try:
        from robot import rebot_cli  # https://robot-framework.readthedocs.io/en/stable/autodoc/robot.html
        rc = rebot_cli(list(args), exit=False)
    except Exception as exc:  # noqa: BLE001
        log.error("rebot failed: %s", exc)
        rc = 3
    _exit(rc)
