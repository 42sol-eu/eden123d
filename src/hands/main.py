import logging
import sys
from abc import ABC, abstractmethod
from typing import List
import click
from rich.console import Console

console = Console()

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.INFO, format=S_LOG_MSG_FORMAT)


class BaseRunner(ABC):
    """Abstract base class for all test runners."""

    @abstractmethod
    def run(self, args: List[str]) -> int:
        """Run the tests with given args and return exit code."""
        pass


class PytestRunner(BaseRunner):
    def run(self, args: List[str]) -> int:
        import pytest  # https://docs.pytest.org/
        logging.debug("Running pytest with args=%s", args)
        return pytest.main(list(args))


class RobotRunner(BaseRunner):
    def run(self, args: List[str]) -> int:
        from robot import run_cli  # https://robot-framework.readthedocs.io/
        logging.debug("Running robot with args=%s", args)
        return run_cli(list(args), exit=False)


class BehaveRunner(BaseRunner):
    def run(self, args: List[str]) -> int:
        from behave.__main__ import main as behave_main  # https://behave.readthedocs.io/
        logging.debug("Running behave with args=%s", args)
        return behave_main(list(args))




RUNTIMES = {
    "pytest": PytestRunner,
    "robot": RobotRunner,
    "behave": BehaveRunner,
}


@click.group()
def cli() -> None:
    """Unified test runner CLI."""


@cli.command(context_settings={"ignore_unknown_options": True})
@click.option("--engine", type=click.Choice(RUNTIMES.keys()), default="pytest", help="Test engine to use")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def run(engine: str, args: tuple[str]) -> None:
    """Run tests with chosen engine."""
    runner_cls = RUNTIMES[engine]
    runner = runner_cls()
    rc = runner.run(list(args))

    if rc == 0:
        console.print(f"[bold green]{engine} tests passed[/bold green]")
    else:
        console.print(f"[bold red]{engine} failed with RC={rc}[/bold red]")
    sys.exit(rc)
