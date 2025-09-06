"""Engine detection logic for automatically determining the appropriate test runner."""
from __future__ import annotations

import importlib.util
import logging
from pathlib import Path
from typing import Dict, List

log = logging.getLogger(__name__)


class EngineDetector:
    """Detects which test engine to use based on files and installed packages.
    TODO: add robot.Gherkin and robot.python
    """
    
    def __init__(self) -> None:
        """Initialize the engine detector."""
        self.supported_engines = ["pytest", "robot", "behave"]
    
    def detect_engine(self, folder: Path, args: List[str]) -> str:
        """
        Detect the appropriate test engine based on file extensions and content.
        
        Args:
            folder: Test folder to analyze
            args: Additional CLI arguments that might contain file paths
            
        Returns:
            Name of the detected engine
            
        Raises:
            RuntimeError: If no suitable engine is found
        """
        log.debug("Detecting engine for folder: %s, args: %s", folder, args)
        
        # Collect all potential file paths from args and folder
        file_paths = self._collect_file_paths(folder, args)
        
        # Check for file-based hints
        engine = self._detect_by_file_extensions(file_paths)
        if engine:
            log.info("Detected engine '%s' based on file extensions", engine)
            return engine
        
        # Check for directory structure hints
        engine = self._detect_by_directory_structure(folder)
        if engine:
            log.info("Detected engine '%s' based on directory structure", engine)
            return engine
        
        # Fallback to installed packages
        engine = self._detect_by_installed_packages()
        if engine:
            log.info("Detected engine '%s' based on installed packages", engine)
            return engine
        
        raise RuntimeError("No supported test engine found")
    
    def get_available_engines(self) -> Dict[str, bool]:
        """
        Get a dictionary of all supported engines and their availability.
        
        Returns:
            Dictionary mapping engine names to their availability status
        """
        availability = {}
        for engine in self.supported_engines:
            availability[engine] = self._is_package_available(engine)
        return availability
    
    def _collect_file_paths(self, folder: Path, args: List[str]) -> List[Path]:
        """Collect all file paths from folder and arguments."""
        file_paths = []
        
        # Add paths from arguments that don't start with "-"
        for arg in args:
            if not arg.startswith("-"):
                path = Path(arg)
                if path.is_absolute():
                    file_paths.append(path)
                else:
                    file_paths.append(folder / path)
        
        # Recursively collect files from the folder
        if folder.exists() and folder.is_dir():
            for pattern in ["**/*.py", "**/*.robot", "**/*.feature"]:
                file_paths.extend(folder.glob(pattern))
        
        return file_paths
    
    def _detect_by_file_extensions(self, file_paths: List[Path]) -> str | None:
        """Detect engine based on file extensions."""
        extension_counts = {".feature": 0, ".robot": 0, ".py": 0}
        test_py_files = 0
        
        for path in file_paths:
            if path.suffix in extension_counts:
                extension_counts[path.suffix] += 1
                
            # Count Python test files specifically
            if path.suffix == ".py" and (
                path.name.startswith("test_") or 
                path.name.endswith("_test.py") or
                "test" in path.parts
            ):
                test_py_files += 1
        
        # Behave has highest priority for .feature files
        if extension_counts[".feature"] > 0:
            return "behave"
        
        # Robot Framework for .robot files
        if extension_counts[".robot"] > 0:
            return "robot"
        
        # Pytest for Python test files
        if test_py_files > 0:
            return "pytest"
        
        return None
    
    def _detect_by_directory_structure(self, folder: Path) -> str | None:
        """Detect engine based on common directory structures."""
        if not folder.exists():
            return None
        
        # Check for behave structure
        features_dir = folder / "features"
        if features_dir.exists() and any(features_dir.glob("*.feature")):
            return "behave"
        
        # Check for pytest structure
        tests_dir = folder / "tests"
        if tests_dir.exists() and any(tests_dir.glob("test_*.py")):
            return "pytest"
        
        # Check for Robot Framework structure
        if any(folder.glob("*.robot")) or any(folder.glob("**/*.robot")):
            return "robot"
        
        return None
    
    def _detect_by_installed_packages(self) -> str | None:
        """Detect engine based on installed packages (fallback)."""
        # Priority order: pytest, robot, behave
        for engine in ["pytest", "robot", "behave"]:
            if self._is_package_available(engine):
                return engine
        return None
    
    def _is_package_available(self, package_name: str) -> bool:
        """Check if a package is available for import."""
        try:
            # Special handling for robot framework
            if package_name == "robot":
                return importlib.util.find_spec("robot") is not None
            return importlib.util.find_spec(package_name) is not None
        except (ImportError, AttributeError, ValueError):
            return False