"""Browser fixtures and viewport-only per-test screenshots."""

from datetime import datetime
from pathlib import Path
import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


PROJECT_ROOT = Path(__file__).resolve().parent
SCREENSHOTS_DIR = PROJECT_ROOT / "artifacts" / "screenshots"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"rep_{outcome.get_result().when}", outcome.get_result())


@pytest.fixture
def driver(request):
    """Start Chrome and save the final browser viewport for each test."""
    options = Options()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)

    try:
        yield browser
    finally:
        try:
            _save_screenshot(browser, _artifact_name(request.node.nodeid), request.node)
        finally:
            browser.quit()


def _artifact_name(test_id):
    safe_test_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", test_id).strip("._")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{safe_test_id}_{timestamp}"


def _save_screenshot(browser, artifact_name, test_node):
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    screenshot_path = SCREENSHOTS_DIR / f"{artifact_name}.png"
    try:
        screenshot_path.write_bytes(browser.get_screenshot_as_png())
        result = getattr(test_node, "rep_call", None)
        status = "passed" if result and result.passed else "failed"
        print(f"\n[artifacts] Screenshot ({status}): {screenshot_path.relative_to(PROJECT_ROOT)}")
    except Exception as error:
        print(f"\n[artifacts] Could not save browser screenshot: {error}")
