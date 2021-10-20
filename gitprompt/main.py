import subprocess

from .parser import PorcelainV2Parser
from .config import Config


class GitPrompt:
    def __init__(self, config: Config):
        self.config = config
        self.parser = PorcelainV2Parser()

    def run(self):
        self.fetch()
        return self.prompt()

    def fetch(self):
        args = ["git", "status", "--porcelain=v2", "--branch"]
        proc = subprocess.run(
            args, shell=False, capture_output=True, timeout=1, text=True,
        )
        self.parser.parse(proc.stdout)

    def prompt(self):
        th = self.config.theme
        gbr = self.parser.branch
        gd = self.parser.directory

        branch = (
            f"{th.branch}{gbr.head or gbr.oid[:8]}{th.rst}"
            + (f"{th.behind}{gbr.behind}{th.rst}" if gbr.behind != 0 else "")
            + (f"{th.ahead}{gbr.ahead}{th.rst}" if gbr.ahead != 0 else "")
        )
        directory = (
            (f"{th.staged}{gd.staged}{th.rst}" if gd.staged != 0 else "")
            + (f"{th.unstaged}{gd.unstaged}{th.rst}" if gd.unstaged != 0 else "")
            + (f"{th.unmerged}{gd.unmerged}{th.rst}" if gd.unmerged != 0 else "")
            + (f"{th.untracked}{gd.untracked}{th.rst}" if gd.untracked != 0 else "")
        )

        prompt = th.prefix + branch + th.separator + (directory or th.clean) + th.suffix
        return prompt
