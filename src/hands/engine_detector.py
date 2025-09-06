"""Engine detection based on file patterns and project structure."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


class EngineDetector:
    """Detects appropriate test engine based on file patterns and project structure."""
    
    def __init__(self) -> None:
        """Initialize the engine detector."""
        pass
    
    def detect_engine(self, test_path: Path) -> str:
        """Detect the most appropriate test engine for the given path.
        
        Args:
            test_path: Path to test directory or file
            
        Returns:
            Engine name: 'pytest', 'robot', or 'behave'
            
        Raises:
            ValueError: If no suitable engine can be detected
        """
        log.debug("Detecting engine for path: %s", test_path)
        
        # Convert to Path if string
        if isinstance(test_path, str):
            test_path = Path(test_path)
            
        # Check if it's a specific file
        if test_path.is_file():
            return self._detect_from_file(test_path)
        
        # Check if it's a directory
        if test_path.is_dir():
            return self._detect_from_directory(test_path)
            
        # If path doesn't exist, try to infer from extension
        return self._detect_from_file(test_path)
    
    def _detect_from_file(self, file_path: Path) -> str:
        """Detect engine from a single file.
        
        Args:
            file_path: Path to test file
            
        Returns:
            Engine name based on file pattern
        """
        suffix = file_path.suffix.lower()
        name = file_path.name.lower()
        
        # Robot Framework files
        if suffix in ['.robot', '.resource']:
            log.debug("Detected Robot Framework file: %s", file_path)
            return 'robot'
        
        # Behave feature files
        if suffix == '.feature':
            log.debug("Detected Behave feature file: %s", file_path)
            return 'behave'
        
        # Python test files - could be pytest
        if suffix == '.py' and ('test_' in name or name.endswith('_test.py')):
            log.debug("Detected Python test file, defaulting to pytest: %s", file_path)
            return 'pytest'
        
        # Default to pytest for Python files
        if suffix == '.py':
            log.debug("Detected Python file, defaulting to pytest: %s", file_path)
            return 'pytest'
        
        # Default fallback
        log.warning("Could not detect engine from file %s, defaulting to pytest", file_path)
        return 'pytest'
    
    def _detect_from_directory(self, dir_path: Path) -> str:
        """Detect engine from directory contents.
        
        Args:
            dir_path: Path to test directory
            
        Returns:
            Engine name based on directory contents
        """
        if not dir_path.exists():
            log.warning("Directory does not exist: %s, defaulting to pytest", dir_path)
            return 'pytest'
        
        # Count different file types
        robot_files = list(dir_path.rglob('*.robot')) + list(dir_path.rglob('*.resource'))
        feature_files = list(dir_path.rglob('*.feature'))
        python_test_files = []
        
        # Find Python test files
        for py_file in dir_path.rglob('*.py'):
            name = py_file.name.lower()
            if 'test_' in name or name.endswith('_test.py') or py_file.parent.name in ['tests', 'test']:
                python_test_files.append(py_file)
        
        log.debug("Found %d robot files, %d feature files, %d python test files", 
                 len(robot_files), len(feature_files), len(python_test_files))
        
        # Decide based on file counts
        if robot_files and len(robot_files) >= len(feature_files) and len(robot_files) >= len(python_test_files):
            log.debug("Most files are Robot Framework, selecting robot engine")
            return 'robot'
        
        if feature_files and len(feature_files) >= len(python_test_files):
            log.debug("Most files are Behave features, selecting behave engine")
            return 'behave'
        
        if python_test_files:
            log.debug("Found Python test files, selecting pytest engine")
            return 'pytest'
        
        # Check for configuration files
        config_files = {
            'pytest': ['pytest.ini', 'pyproject.toml', 'setup.cfg', 'conftest.py'],
            'robot': ['robot.yaml', 'robot.yml'],
            'behave': ['behave.ini', '.behaverc']
        }
        
        for engine, configs in config_files.items():
            for config in configs:
                if (dir_path / config).exists():
                    log.debug("Found %s config file, selecting %s engine", config, engine)
                    return engine
        
        # Default fallback
        log.warning("Could not detect engine from directory %s, defaulting to pytest", dir_path)
        return 'pytest'
