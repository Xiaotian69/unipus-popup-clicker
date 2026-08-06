import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def read_project_file(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_run_windows_prompts_for_and_quotes_explicit_url():
    script = read_project_file("run_windows.bat")

    assert 'set /p "TARGET_URL=' in script
    assert "if not defined TARGET_URL" in script
    assert 'popup_clicker.py --url "%TARGET_URL%"' in script


@pytest.mark.parametrize(
    "command",
    [
        '".venv\\Scripts\\python.exe" -m pip install --upgrade pip',
        '".venv\\Scripts\\python.exe" -m pip install -r requirements.txt',
        '".venv\\Scripts\\python.exe" -m playwright install chromium',
        '".venv\\Scripts\\python.exe" -m pytest -q',
    ],
)
def test_setup_windows_fails_immediately_after_required_step(command: str):
    script = read_project_file("setup_windows.bat")
    guarded_command = re.escape(command) + r"\s*\nif errorlevel 1 goto :failed"

    assert re.search(guarded_command, script)


def test_setup_windows_success_message_cannot_run_after_failure():
    script = read_project_file("setup_windows.bat")

    assert re.search(r"echo Setup complete\.[\s\S]*?exit /b 0\s*\n\s*:failed", script)
    assert "echo Setup failed." in script
    assert script.rstrip().endswith("exit /b 1")


def test_terminal_browser_asset_is_disclosed_as_synthetic():
    source = read_project_file("docs/assets/screenshots/terminal-and-browser-source.html")
    readme = read_project_file("README.md")

    assert "Illustrative synthetic demo" in source
    assert "Illustrative synthetic demo" in readme
    assert "popup state transition" in readme
