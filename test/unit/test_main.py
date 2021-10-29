import pytest
from unittest.mock import Mock

from types import SimpleNamespace as SN
from subprocess import CompletedProcess, CalledProcessError

import gitprompt.main as module


# {{{ Fakes
class FakeParser:
    def parse(self, text):
        self.branch = SN(
            head="head",
            oid="oid",
            behind=1,
            ahead=0,
        )
        self.directory = SN(
            staged=1,
            unstaged=0,
            unmerged=0,
            untracked=2,
        )


# }}}


# {{{ Fixtures
theme = SN(
    prefix="[",
    suffix="]",
    behind="-",
    ahead="+",
    separator=" -- ",
    branch="br:",
    staged="+",
    unstaged="!",
    unmerged="m",
    untracked="?",
    clean="CLEAN",
    rst="X",
)
config = module.Config(theme)


# }}}


def test_prompt(monkeypatch):
    monkeypatch.setattr(module, "PorcelainV2Parser", FakeParser)

    gp = module.GitPrompt(config)
    gp.parser.parse("whatever")

    prompt = gp.prompt()

    assert prompt == "[br:headX-1X -- +1X?2X]"


def test_fetch(monkeypatch):
    def fake_sprun(args, **_):
        assert " ".join(args) == "git status --porcelain=v2 --branch"

        return CompletedProcess(args=args, returncode=0, stdout="some porcelain")

    monkeypatch.setattr("subprocess.run", fake_sprun)
    monkeypatch.setattr(module, "PorcelainV2Parser", Mock(autospec=True))

    gp = module.GitPrompt(config)
    gp.fetch()

    gp.parser.parse.assert_called_once_with("some porcelain")

def test_run_ok(monkeypatch):
    def fake_sprun(args, **_):
        return CompletedProcess(args=args, returncode=0, stdout="whatever")
    monkeypatch.setattr("subprocess.run", fake_sprun)
    monkeypatch.setattr(module, "PorcelainV2Parser", FakeParser)

    gp = module.GitPrompt(config)
    prompt = gp.run()

    assert prompt != ""

def test_run_nogit(monkeypatch):
    def fake_sprun(args, **_):
        raise CalledProcessError(returncode=128, cmd=args)
    monkeypatch.setattr("subprocess.run", fake_sprun)
    monkeypatch.setattr(module, "PorcelainV2Parser", Mock(autospec=True))

    gp = module.GitPrompt(config)
    prompt = gp.run()

    assert prompt == ""
    gp.parser.parse.assert_not_called()
