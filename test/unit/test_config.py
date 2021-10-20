import pytest

import gitprompt.config as module


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("GITPROMPT_THEME_PREFIX", "[")
    monkeypatch.setenv("GITPROMPT_THEME_SUFFIX", "]")
    monkeypatch.setenv("WRONG_PREFIX_BRANCH", "branch")
    monkeypatch.setenv("GITPROMPT_THEME_CONFLICTS", "conflicts")
    monkeypatch.delenv("GITPROMPT_THEME_UNTRACKES", raising=False)

    config = module.Config.from_env()

    assert config.theme.prefix == "["
    assert config.theme.suffix == "]"
    assert config.theme.branch == ""
    assert config.theme.unmerged == "conflicts"
    assert config.theme.untracked == ""
