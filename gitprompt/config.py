import os
from typing import Self


class Theme:
    _ENV = {
        "prefix": "PREFIX",
        "suffix": "SUFFIX",
        "branch": "BRANCH",
        "behind": "BEHIND",
        "ahead": "AHEAD",
        "separator": "SEPARATOR",
        "staged": "STAGED",
        "unstaged": "CHANGED",
        "unmerged": "CONFLICTS",
        "untracked": "UNTRACKED",
        "clean": "CLEAN",
    }

    def __init__(
        self,
        *,
        suffix: str = "",
        prefix: str = "",
        branch: str = "",
        behind: str = "",
        ahead: str = "",
        separator: str = "",
        staged: str = "",
        unstaged: str = "",
        unmerged: str = "",
        untracked: str = "",
        clean: str = "",
    ) -> None:
        self.suffix = suffix
        self.prefix = prefix
        self.branch = branch
        self.behind = behind
        self.ahead = ahead
        self.separator = separator
        self.staged = staged
        self.unstaged = unstaged
        self.unmerged = unmerged
        self.untracked = untracked
        self.clean = clean

    @property
    def rst(self) -> str:
        # The following does not work because for some reasons the `$reset_color` is not
        # extended. However, manually extending it produces the expected result.
        # return "%{$reset_color%}"
        return b"%{\x1b[00m%}".decode()

    @classmethod
    def from_env(cls, prefix="GITPROMPT_THEME_") -> Self:
        kwargs = {}
        for arg, env in cls._ENV.items():
            try:
                kwargs[arg] = os.environ[prefix + env]
            except KeyError:
                pass
        return cls(**kwargs)


class Config:
    def __init__(self, theme: Theme) -> None:
        self.theme = theme

    @classmethod
    def from_env(cls) -> Self:
        return cls(theme=Theme.from_env())
