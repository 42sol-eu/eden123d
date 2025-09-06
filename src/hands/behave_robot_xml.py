"""Behave formatter that emits Robot-style output.xml."""
from __future__ import annotations

import logging  # https://docs.python.org/3/library/logging.html
from datetime import datetime, timezone  # https://docs.python.org/3/library/datetime.html
from typing import List  # https://docs.python.org/3/library/typing.html

from behave.formatter.base import Formatter  # https://behave.readthedocs.io/
from behave.model_core import Status  # https://behave.readthedocs.io/

from .report_xml import TestResult, write_robot_output  # local util

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.INFO, format=S_LOG_MSG_FORMAT)
logger = logging.getLogger(__name__)


class RobotXmlFormatter(Formatter):
    """Collects scenario results and writes Robot XML on close()."""

    def __init__(self, stream, config) -> None:  # noqa: D401
        super().__init__(stream, config)
        self.results: List[TestResult] = []
        self.suite_name = getattr(config, "robot_suite_name", "Behave Suite")
        # Get output file from config.outfile, which behave sets from --outfile
        self.out_path = getattr(config, "outfile", "output.xml")
        if hasattr(config, "outputs") and config.outputs:
            # Use the first output file if multiple are specified
            self.out_path = config.outputs[0].name
        self.features = []

    def feature(self, feature) -> None:
        """Record feature for later processing."""
        self.features.append(feature)

    def scenario(self, scenario) -> None:
        """Record scenario start."""
        scenario._robotic_start = datetime.now(tz=timezone.utc)  # type: ignore[attr-defined]

    def result(self, step) -> None:  # not used; we keep minimal body
        """We could aggregate per-step messages here if desired."""

    def scenario_outline(self, outline) -> None:
        """No special handling needed for outlines in minimal model."""

    def eof(self) -> None:
        """End of file reached."""

    def close(self) -> None:
        """At the end, convert all scenarios to TestResult and write XML."""
        for feature in self.features:
            for scenario in feature.scenarios:
                start = getattr(scenario, "_robotic_start", datetime.now(tz=timezone.utc))
                end = datetime.now(tz=timezone.utc)
                status_map = {
                    Status.passed: "PASS",
                    Status.failed: "FAIL",
                    Status.skipped: "SKIP",
                    Status.untested: "SKIP"
                }
                status = status_map.get(scenario.status, "FAIL")
                message = None
                if scenario.status is Status.failed and scenario.exception:
                    message = str(scenario.exception)[:2000]
                tags = [t for t in scenario.tags] if scenario.tags else None
                self.results.append(
                    TestResult(
                        name=f"{feature.name} :: {scenario.name}",
                        status=status,
                        start=start,
                        end=end,
                        message=message,
                        tags=tags
                    )
                )
        try:
            if self.results:  # Only write if we have results
                write_robot_output(self.suite_name, self.results, self.out_path)
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed writing Robot XML: %s", exc)
