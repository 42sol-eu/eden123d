"""Pytest plugin that emits Robot-style output.xml at session end."""
from __future__ import annotations

import logging  # https://docs.python.org/3/library/logging.html
from datetime import datetime, timezone  # https://docs.python.org/3/library/datetime.html
from typing import Dict, List  # https://docs.python.org/3/library/typing.html
import pytest  # https://docs.pytest.org/  # noqa: F401

from .report_xml import TestResult, write_robot_output  # local util

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.INFO, format=S_LOG_MSG_FORMAT)
logger = logging.getLogger(__name__)


def pytest_addoption(parser) -> None:
    """Add --robot-output to configure where to write output.xml."""
    group = parser.getgroup("robotxml")
    group.addoption(
        "--robot-output",
        action="store",
        dest="robot_output",
        default="output.xml",
        help="Path to Robot-style output.xml to generate"
    )
    group.addoption(
        "--robot-suite-name",
        action="store",
        dest="robot_suite_name",
        default="Pytest Suite",
        help="Suite name in Robot XML"
    )


class _Store:
    """Collects per-test timing and results."""
    def __init__(self) -> None:
        self.starts: Dict[str, datetime] = {}
        self.results: List[TestResult] = []


_store = _Store()


def pytest_runtest_protocol(item, nextitem) -> None:  # noqa: ANN001 (pytest signature)
    """Capture start times for every test item."""
    _store.starts[item.nodeid] = datetime.now(tz=timezone.utc)


def pytest_runtest_logreport(report) -> None:  # noqa: ANN001 (pytest signature)
    """Collect outcome and end time for call phase."""
    if report.when != "call":
        return
    start = _store.starts.get(report.nodeid, datetime.now(tz=timezone.utc))
    end = datetime.now(tz=timezone.utc)
    status = "PASS" if report.passed else ("SKIP" if report.skipped else "FAIL")
    message = None
    if report.failed and hasattr(report, "longrepr"):
        # Trim longrepr to a shorter message; full traceback remains in pytest artifacts
        message = str(report.longrepr)[:2000]
    _store.results.append(
        TestResult(
            name=report.nodeid,
            status=status,
            start=start,
            end=end,
            message=message,
            tags=None
        )
    )


def pytest_sessionfinish(session, exitstatus) -> None:  # noqa: ANN001 (pytest signature)
    """Write Robot XML at session end."""
    try:
        path = session.config.getoption("robot_output")
        suite_name = session.config.getoption("robot_suite_name")
        write_robot_output(suite_name, _store.results, path)
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed writing Robot XML: %s", exc)
