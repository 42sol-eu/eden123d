"""Unified CLI that can run with pytest/behave/robot and produce Robot XML."""
from __future__ import annotations

import logging  # https://docs.python.org/3/library/logging.html
import sys  # https://docs.python.org/3/library/sys.html
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html
from typing import List, Optional  # https://docs.python.org/3/library/typing.html

import typer  # https://typer.tiangolo.com/
from rich.console import Console  # https://rich.readthedocs.io/

from .engine_detector import EngineDetector
from .test_engines import TestEngineFactory

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


@app.command("run")
def run(
    test_path: str = typer.Argument(".", help="Path to test directory or file"),
    engine: Optional[str] = typer.Option(None, "--engine", "-e",
                                       help="pytest | robot | behave (auto-detect if not specified)"),
    output: str = typer.Option("output.xml", "--output", "-o",
                              help="Path to Robot-style output.xml file"),
    suite_name: Optional[str] = typer.Option(None, "--suite-name", "-s",
                                           help="Suite name in Robot XML (auto-generated if not specified)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logging"),
    args: List[str] = typer.Argument(None, help="Additional arguments passed to the test engine"),
) -> None:
    """Run tests with the chosen engine, forwarding arguments.
    
    The engine can be auto-detected based on test file patterns or explicitly specified.
    All additional arguments are passed through to the underlying test engine.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    log.debug("run(test_path=%s, engine=%s, output=%s, suite_name=%s, args=%s)", 
              test_path, engine, output, suite_name, args)
    
    # Auto-detect engine if not specified
    if engine is None:
        detector = EngineDetector()
        engine = detector.detect_engine(Path(test_path))
        console.print(f"[blue]Auto-detected engine: {engine}[/blue]")
    
    # Auto-generate suite name if not specified  
    if suite_name is None:
        suite_name = f"{engine.title()} Test Suite - {Path(test_path).name}"
    
    rc = 1
    try:
        factory = TestEngineFactory()
        test_engine = factory.create_engine(engine)
        rc = test_engine.run_tests(
            test_path=Path(test_path),
            output_file=output,
            suite_name=suite_name,
            engine_args=args or []
        )
    except Exception as exc:  # noqa: BLE001
        log.error("Engine failed: %s", exc)
        rc = 3
    _exit(rc)


@app.command("report")
def report(
    input_files: List[str] = typer.Argument(..., help="Robot XML files to combine"),
    output: str = typer.Option("report.html", "--output", "-o", help="Output HTML report file"),
    args: List[str] = typer.Option([], "--args", help="Additional arguments passed to rebot"),
) -> None:
    """Generate combined HTML reports from Robot XML files using rebot.
    
    This command leverages robotframework's rebot tool to create unified reports
    from multiple output.xml files, regardless of which test engines generated them.
    """
    log.debug("report(input_files=%s, output=%s, args=%s)", input_files, output, args)
    
    # Build rebot command arguments
    rebot_args = []
    rebot_args.extend(["--output", "NONE"])  # Don't generate output.xml
    rebot_args.extend(["--report", output])
    rebot_args.extend(args)  # Additional user arguments
    rebot_args.extend(input_files)  # Input XML files
    
    try:
        from robot import rebot_cli  # https://robot-framework.readthedocs.io/en/stable/autodoc/robot.html
        rc = rebot_cli(rebot_args, exit=False)
        if rc == 0:
            console.print(f"[green]Report generated: {output}[/green]")
    except Exception as exc:  # noqa: BLE001
        log.error("rebot failed: %s", exc)
        rc = 3
    _exit(rc)


def cli() -> None:
    """CLI entry point."""
    app()


if __name__ == "__main__":
    cli()
