"""Behave formatter that emits Robot-style output.xml."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import List

from behave.formatter.base import Formatter
from behave.model_core import Status

from .report_xml import TestResult, write_robot_output

log = logging.getLogger(__name__)


class RobotXmlFormatter(Formatter):
    """Collects scenario results and writes Robot XML on close()."""

    def __init__(self, stream, config) -> None:
        """Initialize the formatter."""
        super().__init__(stream, config)
        self.results: List[TestResult] = []
        self.suite_name = getattr(config, "robot_suite_name", "Behave Suite")
        
        # Get output file from config or use default
        self.out_path = getattr(config, "output_file", "output.xml")
        if hasattr(config, "outfile") and config.outfile:
            # Use the outfile if specified via --outfile
            self.out_path = config.outfile.name if hasattr(config.outfile, 'name') else str(config.outfile)
    
    def feature(self, feature) -> None:
        """Called when a feature starts."""
        self.current_feature = feature
    
    def scenario(self, scenario) -> None:
        """Record scenario start time."""
        scenario._robotic_start = datetime.now(tz=timezone.utc)
    
    def result(self, step) -> None:
        """Called when a step completes - not used in minimal model."""
        pass
    
    def scenario_outline(self, outline) -> None:
        """Handle scenario outlines - no special handling needed."""
        pass
    
    def eof(self) -> None:
        """End of file reached."""
        pass
    
    def close(self) -> None:
        """Convert all scenarios to TestResult and write XML."""
        log.debug("RobotXmlFormatter.close() called")
        
        # Collect results from all features
        try:
            # Try to access features from the formatter's stream context
            if hasattr(self, 'features'):
                features = self.features
            elif hasattr(self.stream, 'features'):
                features = self.stream.features
            else:
                # Fallback: try to get from config
                features = getattr(self.config, 'features', [])
            
            for feature in features:
                for scenario in feature.scenarios:
                    self._process_scenario(feature, scenario)
                    
        except (AttributeError, TypeError) as exc:
            log.warning("Could not access features from formatter context: %s", exc)
            # If we can't access features, try to use any accumulated results
        
        # Write the XML output
        if self.results:
            try:
                write_robot_output(self.suite_name, self.results, self.out_path)
                log.info("Wrote Robot XML with %d test results to %s", len(self.results), self.out_path)
            except Exception as exc:
                log.error("Failed writing Robot XML: %s", exc)
        else:
            log.warning("No test results collected for Robot XML output")
    
    def _process_scenario(self, feature, scenario) -> None:
        """Process a single scenario into a TestResult."""
        start = getattr(scenario, "_robotic_start", datetime.now(tz=timezone.utc))
        end = datetime.now(tz=timezone.utc)
        
        # Map behave status to Robot status
        status_map = {
            Status.passed: "PASS",
            Status.failed: "FAIL",
            Status.skipped: "SKIP",
            Status.untested: "SKIP"
        }
        status = status_map.get(scenario.status, "FAIL")
        
        # Collect error message if failed
        message = None
        if scenario.status == Status.failed:
            if hasattr(scenario, 'exception') and scenario.exception:
                message = str(scenario.exception)[:2000]
            elif hasattr(scenario, 'error_message'):
                message = scenario.error_message[:2000]
        
        # Collect tags
        tags = list(scenario.tags) if scenario.tags else None
        
        # Create test result
        test_result = TestResult(
            name=f"{feature.name} :: {scenario.name}",
            status=status,
            start=start,
            end=end,
            message=message,
            tags=tags
        )
        
        self.results.append(test_result)
        log.debug("Added test result: %s (%s)", test_result.name, test_result.status)
