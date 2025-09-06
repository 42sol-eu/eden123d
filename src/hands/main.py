"""Unified CLI that can run with pytest/behave/robot and produce Robot XML."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from .engine_detector import EngineDetector
from .test_engines import TestEngineFactory
from snark import snark_cite

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)-5.5s] %(message)s")
log = logging.getLogger(__name__)
console = Console()

# Create CLI app
app = typer.Typer(help="Unified test runner that can emit Robot-style output.xml")


def _exit(rc: int) -> None:
    """Exit helper to keep cyclomatic complexity low."""
    quote = snark_cite()
    if rc == 0:
        log.info(quote)
    else:
        log.info(f"{quote}. RC=%s", rc)
    raise typer.Exit(code=rc)


@app.command()
def run(
    engine: Optional[str] = typer.Option(None, "--engine", "-e", help="pytest | robot | behave"),
    folder: str = typer.Option(".", "--folder", "-f", help="Test folder to run"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    output: str = typer.Option("output.xml", "--output", "-o", help="Output XML file"),
    args: Optional[List[str]] = typer.Argument(None, help="Additional arguments passed to the engine"),
) -> None:
    """Run tests with the chosen or auto-detected engine."""
    log.debug("run(engine=%s, folder=%s, args=%s)", engine, folder, args)
    
    # Detect engine if not specified
    if not engine:
        detector = EngineDetector()
        engine = detector.detect_engine(Path(folder), args or [])
        console.print(f"[green]Auto-detected test engine: {engine}[/green]")
    
    # Create and configure the test engine
    try:
        test_engine = TestEngineFactory.create_engine(engine)
        rc = test_engine.run_tests(
            folder=Path(folder),
            output_file=output,
            verbose=verbose,
            extra_args=args or []
        )
    except Exception as exc:
        log.error("Engine failed: %s", exc)
        rc = 3
    
    _exit(rc)


@app.command()
def report(
    output_files: List[str] = typer.Argument(..., help="Robot XML output files to combine"),
    report_file: str = typer.Option("report.html", "--report", "-r", help="Combined HTML report file"),
    log_file: str = typer.Option("log.html", "--log", "-l", help="Combined log file"),
) -> None:
    """Generate combined HTML reports from Robot XML output files using rebot.
    TODO: allow passing in wild cards.
    """
    log.debug("report(output_files=%s, report_file=%s)", output_files, report_file)
    
    try:
        from robot import rebot_cli
        
        # Build rebot arguments
        rebot_args = [
            "--report", report_file,
            "--log", log_file,
            "--outputdir", ".",
        ] + output_files
        
        console.print(f"[blue]Generating combined report from {len(output_files)} files...[/blue]")
        rc = rebot_cli(rebot_args, exit=False)
        
        if rc == 0:
            console.print(f"[green]Combined report generated: {report_file}[/green]")
        else:
            console.print(f"[red]Report generation failed with exit code: {rc}[/red]")
            
    except Exception as exc:
        log.error("rebot failed: %s", exc)
        rc = 3
    
    _exit(rc)


@app.command()
def list_engines() -> None:
    """List available test engines and their status."""
    detector = EngineDetector()
    available_engines = detector.get_available_engines()
    
    console.print("[bold]Available Test Engines:[/bold]")
    for engine_name, is_available in available_engines.items():
        status = "[green]✓[/green]" if is_available else "[red]✗[/red]"
        console.print(f"  {status} {engine_name}")


def cli() -> None:
    """Main CLI entry point."""
    app()
