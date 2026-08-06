from pathlib import Path

import pytest

from popup_clicker import Settings, build_button_patterns, parse_args


CONFIRM_TEXT = "\u786e\u5b9a"


def test_settings_defaults_are_safe():
    settings = Settings(url="https://example.com/notifications")

    assert settings.button_text == CONFIRM_TEXT
    assert settings.poll_seconds >= 1
    assert settings.profile_dir == Path(".browser-profile")
    assert "password" not in repr(settings).lower()
    assert "apikey" not in repr(settings).lower()


def test_parse_args_requires_explicit_url():
    with pytest.raises(SystemExit) as exc_info:
        parse_args([])

    assert exc_info.value.code == 2


def test_parse_args_accepts_explicit_url():
    settings = parse_args(["--url", "https://example.com/notifications"])

    assert settings.url == "https://example.com/notifications"


def test_build_button_patterns_includes_text_and_clickable_selectors():
    patterns = build_button_patterns(CONFIRM_TEXT)

    assert patterns[0] == CONFIRM_TEXT
    assert f'button:has-text("{CONFIRM_TEXT}")' in patterns
    assert f'[role=button]:has-text("{CONFIRM_TEXT}")' in patterns


def test_settings_rejects_too_fast_polling():
    with pytest.raises(ValueError, match="poll_seconds"):
        Settings(url="https://example.com/notifications", poll_seconds=0.2)
