import logging  # https://docs.python.org/3/library/logging.html
import sys
import click  # https://click.palletsprojects.com/
from rich.console import Console  # https://rich.readthedocs.io/
from robot import run_cli, rebot_cli  # https://robot-framework.readthedocs.io/
from robot.tidy import Tidy  # https://robot-framework.readthedocs.io/en/stable/tools/Tidy.html
from robot.libdoc import libdoc_cli  # https://robot-framework.readthedocs.io/en/stable/tools/Libdoc.html
from robot.testdoc import testdoc_cli  # https://robot-framework.readthedocs.io/en/stable/tools/Testdoc.html
from robot.testsplit import testsplit_cli  # https://robot-framework.readthedocs.io/en/stable/tools/Testsplit.html

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.INFO, format=S_LOG_MSG_FORMAT)

console = Console()


@click.group()
def cli() -> None:
    """Pythonic CLI wrapper for Robot Framework tools."""
    pass


# -------------------------
# Runner: robot
# -------------------------
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def run(args: tuple[str]) -> None:
    """Run Robot Framework test suites."""
    logging.debug("run(args=%s)", args)
    rc = run_cli(list(args), exit=False)
    if rc == 0:
        console.print("[bold green]All tests passed![/bold green]")
    else:
        console.print(f"[bold red]{rc} test(s) failed[/bold red]")
    sys.exit(rc)


# -------------------------
# Reprocessor: rebot
# -------------------------
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def report(args: tuple[str]) -> None:
    """Re-process Robot Framework outputs."""
    logging.debug("report(args=%s)", args)
    rc = rebot_cli(list(args), exit=False)
    if rc == 0:
        console.print("[bold green]Report generated successfully![/bold green]")
    else:
        console.print(f"[bold red]Rebot failed with RC={rc}[/bold red]")
    sys.exit(rc)


# -------------------------
# Formatter: tidy
# -------------------------
@cli.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True))
@click.option("--inplace", is_flag=True, help="Modify files in place")
def tidy(paths: tuple[str], inplace: bool) -> None:
    """Reformat Robot Framework data files."""
    logging.debug("tidy(paths=%s, inplace=%s)", paths, inplace)
    tidy = Tidy(in_place=inplace)
    for path in paths:
        tidy.file(path)
        console.print(f"[cyan]Tidied:[/cyan] {path}")


# -------------------------
# Documentation: libdoc
# -------------------------
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def libdoc(args: tuple[str]) -> None:
    """Generate keyword documentation for libraries."""
    logging.debug("libdoc(args=%s)", args)
    rc = libdoc_cli(list(args))
    sys.exit(rc)


# -------------------------
# Documentation: testdoc
# -------------------------
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def testdoc(args: tuple[str]) -> None:
    """Generate high-level documentation for test suites."""
    logging.debug("testdoc(args=%s)", args)
    rc = testdoc_cli(list(args))
    sys.exit(rc)


# -------------------------
# Suite splitter: testsplit
# -------------------------
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def testsplit(args: tuple[str]) -> None:
    """Split test suites for parallel execution."""
    logging.debug("testsplit(args=%s)", args)
    rc = testsplit_cli(list(args))
    sys.exit(rc)


if __name__ == "__main__":
    cli()
