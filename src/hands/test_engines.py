"""Test engine abstractions and factory for running different test frameworks."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

log = logging.getLogger(__name__)


class TestEngine(ABC):
    """Abstract base class for test engines."""
    
    @abstractmethod
    def run_tests(
        self, 
        test_path: Path, 
        output_file: str, 
        suite_name: str, 
        engine_args: List[str]
    ) -> int:
        """Run tests and generate Robot XML output.
        
        Args:
            test_path: Path to test directory or file
            output_file: Path to output XML file
            suite_name: Name for the test suite
            engine_args: Additional arguments to pass to the engine
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        pass


class PytestEngine(TestEngine):
    """Pytest test engine implementation."""
    
    def run_tests(
        self, 
        test_path: Path, 
        output_file: str, 
        suite_name: str, 
        engine_args: List[str]
    ) -> int:
        """Run pytest tests with Robot XML output.
        
        Args:
            test_path: Path to test directory or file
            output_file: Path to output XML file
            suite_name: Name for the test suite
            engine_args: Additional arguments to pass to pytest
            
        Returns:
            Exit code from pytest
        """
        log.info("Running pytest on %s, output: %s", test_path, output_file)
        
        try:
            import pytest
            
            # Build pytest arguments
            pytest_args = [
                str(test_path),
                f"--robot-output={output_file}",
                f"--robot-suite-name={suite_name}",
            ]
            pytest_args.extend(engine_args)
            
            log.debug("Pytest arguments: %s", pytest_args)
            return pytest.main(pytest_args)
            
        except ImportError as exc:
            log.error("Pytest not available: %s", exc)
            return 1
        except Exception as exc:
            log.error("Pytest execution failed: %s", exc)
            return 1


class RobotEngine(TestEngine):
    """Robot Framework test engine implementation."""
    
    def run_tests(
        self, 
        test_path: Path, 
        output_file: str, 
        suite_name: str, 
        engine_args: List[str]
    ) -> int:
        """Run Robot Framework tests.
        
        Args:
            test_path: Path to test directory or file
            output_file: Path to output XML file
            suite_name: Name for the test suite
            engine_args: Additional arguments to pass to robot
            
        Returns:
            Exit code from robot
        """
        log.info("Running Robot Framework on %s, output: %s", test_path, output_file)
        
        try:
            from robot import run_cli
            
            # Build robot arguments
            robot_args = [
                "--output", output_file,
                "--name", suite_name,
            ]
            robot_args.extend(engine_args)
            robot_args.append(str(test_path))
            
            log.debug("Robot arguments: %s", robot_args)
            return run_cli(robot_args, exit=False)
            
        except ImportError as exc:
            log.error("Robot Framework not available: %s", exc)
            return 1
        except Exception as exc:
            log.error("Robot Framework execution failed: %s", exc)
            return 1


class BehaveEngine(TestEngine):
    """Behave test engine implementation."""
    
    def run_tests(
        self, 
        test_path: Path, 
        output_file: str, 
        suite_name: str, 
        engine_args: List[str]
    ) -> int:
        """Run Behave tests with Robot XML output.
        
        Args:
            test_path: Path to test directory or file
            output_file: Path to output XML file
            suite_name: Name for the test suite
            engine_args: Additional arguments to pass to behave
            
        Returns:
            Exit code from behave
        """
        log.info("Running Behave on %s, output: %s", test_path, output_file)
        
        try:
            from behave.__main__ import main as behave_main
            
            # Build behave arguments
            behave_args = [
                str(test_path),
                "--format", "hands.behave_robot_xml:RobotXmlFormatter",
                "--outfile", output_file,
            ]
            behave_args.extend(engine_args)
            
            log.debug("Behave arguments: %s", behave_args)
            return behave_main(behave_args)
            
        except ImportError as exc:
            log.error("Behave not available: %s", exc)
            return 1
        except Exception as exc:
            log.error("Behave execution failed: %s", exc)
            return 1


class TestEngineFactory:
    """Factory for creating test engine instances."""
    
    def __init__(self) -> None:
        """Initialize the factory."""
        self._engines = {
            'pytest': PytestEngine,
            'robot': RobotEngine,
            'behave': BehaveEngine,
        }
    
    def create_engine(self, engine_name: str) -> TestEngine:
        """Create a test engine instance.
        
        Args:
            engine_name: Name of the engine ('pytest', 'robot', 'behave')
            
        Returns:
            TestEngine instance
            
        Raises:
            ValueError: If engine_name is not supported
        """
        if engine_name not in self._engines:
            available = ', '.join(self._engines.keys())
            raise ValueError(f"Unknown engine '{engine_name}'. Available: {available}")
        
        engine_class = self._engines[engine_name]
        return engine_class()
    
    def get_available_engines(self) -> List[str]:
        """Get list of available engine names.
        
        Returns:
            List of engine names
        """
        return list(self._engines.keys())
