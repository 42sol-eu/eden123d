"""Test engine implementations for different test frameworks."""
from __future__ import annotations

import logging
import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

log = logging.getLogger(__name__)


class BaseTestEngine(ABC):
    """Abstract base class for test engines."""
    
    def __init__(self, name: str) -> None:
        """Initialize the test engine with a name."""
        self.name = name
        
    @abstractmethod
    def run_tests(
        self, 
        folder: Path, 
        output_file: str, 
        verbose: bool = False,
        extra_args: List[str] | None = None
    ) -> int:
        """
        Run tests and generate Robot Framework compatible output.
        
        Args:
            folder: Test folder to run
            output_file: Output XML file path
            verbose: Enable verbose output
            extra_args: Additional arguments to pass to the test runner
            
        Returns:
            Exit code from the test run
        """
        pass


class PytestEngine(BaseTestEngine):
    """Pytest test engine that generates Robot Framework XML."""
    
    def __init__(self) -> None:
        """Initialize the pytest engine."""
        super().__init__("pytest")
    
    def run_tests(
        self, 
        folder: Path, 
        output_file: str, 
        verbose: bool = False,
        extra_args: List[str] | None = None
    ) -> int:
        """Run pytest tests with Robot XML output."""
        try:
            import pytest
            
            # Build pytest arguments
            args = [
                str(folder),
                f"--robot-output={output_file}",
                "--robot-suite-name=Pytest Suite",
            ]
            
            if verbose:
                args.append("-v")
            
            # Add extra arguments
            if extra_args:
                args.extend(extra_args)
            
            log.info("Running pytest with args: %s", args)
            return pytest.main(args)
            
        except ImportError:
            log.error("Pytest is not installed")
            return 1
        except Exception as exc:
            log.error("Pytest execution failed: %s", exc)
            return 1


class RobotEngine(BaseTestEngine):
    """Robot Framework test engine."""
    
    def __init__(self) -> None:
        """Initialize the Robot Framework engine."""
        super().__init__("robot")
    
    def run_tests(
        self, 
        folder: Path, 
        output_file: str, 
        verbose: bool = False,
        extra_args: List[str] | None = None
    ) -> int:
        """Run Robot Framework tests."""
        try:
            from robot import run_cli
            
            # Build robot arguments
            args = [
                "--output", output_file,
                "--outputdir", str(folder.parent),
            ]
            
            if verbose:
                args.extend(["--loglevel", "DEBUG"])
            
            # Add extra arguments
            if extra_args:
                args.extend(extra_args)
            
            # Add test folder/files
            args.append(str(folder))
            
            log.info("Running robot with args: %s", args)
            return run_cli(args, exit=False)
            
        except ImportError:
            log.error("Robot Framework is not installed")
            return 1
        except Exception as exc:
            log.error("Robot Framework execution failed: %s", exc)
            return 1


class BehaveEngine(BaseTestEngine):
    """Behave test engine that generates Robot Framework XML."""
    
    def __init__(self) -> None:
        """Initialize the behave engine."""
        super().__init__("behave")
    
    def run_tests(
        self, 
        folder: Path, 
        output_file: str, 
        verbose: bool = False,
        extra_args: List[str] | None = None
    ) -> int:
        """Run behave tests with Robot XML output."""
        try:
            # Build behave arguments
            args = [
                sys.executable, "-m", "behave",
                "--format", "hands.behave_robot_xml:RobotXmlFormatter",
                "--outfile", output_file,
                str(folder),
            ]
            
            if verbose:
                args.extend(["--verbose"])
            
            # Add extra arguments
            if extra_args:
                args.extend(extra_args)
            
            log.info("Running behave with args: %s", args)
            result = subprocess.run(args, capture_output=False)
            return result.returncode
            
        except Exception as exc:
            log.error("Behave execution failed: %s", exc)
            return 1


class GherkinPytestEngine(BaseTestEngine):
    """Gherkin parser with pytest execution engine."""
    
    def __init__(self) -> None:
        """Initialize the gherkin-pytest engine."""
        super().__init__("gherkin-pytest")
    
    def run_tests(
        self, 
        folder: Path, 
        output_file: str, 
        verbose: bool = False,
        extra_args: List[str] | None = None
    ) -> int:
        """Run gherkin features through pytest."""
        # This would be implemented with a gherkin parser
        # For now, placeholder implementation
        log.warning("Gherkin-pytest engine not yet fully implemented")
        return 1


class TestEngineFactory:
    """Factory for creating test engine instances."""
    
    _engines = {
        "pytest": PytestEngine,
        "robot": RobotEngine,
        "behave": BehaveEngine,
        "gherkin-pytest": GherkinPytestEngine,
    }
    
    @classmethod
    def create_engine(cls, engine_name: str) -> BaseTestEngine:
        """
        Create a test engine instance.
        
        Args:
            engine_name: Name of the engine to create
            
        Returns:
            Test engine instance
            
        Raises:
            ValueError: If engine name is not supported
        """
        if engine_name not in cls._engines:
            available = ", ".join(cls._engines.keys())
            raise ValueError(f"Unknown engine '{engine_name}'. Available: {available}")
        
        engine_class = cls._engines[engine_name]
        return engine_class()
    
    @classmethod
    def get_available_engines(cls) -> List[str]:
        """Get list of available engine names."""
        return list(cls._engines.keys())