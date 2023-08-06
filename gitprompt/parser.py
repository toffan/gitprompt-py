import re


class PorcelainV2Parser:

    """ Parse status information from a porcelain v2 status
    """

    def __init__(self):
        self.branch = BranchParser()
        self.directory = DirectoryParser()

    def parse(self, porcelain: str):
        lines = PorcelainV2Parser.clean(porcelain)
        for line in lines:
            if line.startswith("# "):
                self.branch.update(line[2:].strip())
            else:
                self.directory.update(line.strip())

    @staticmethod
    def clean(text: str):
        stripped = (line.strip() for line in text.splitlines())
        return [line for line in stripped if line]


class BranchParser:

    """ Parse branch information from a porcelain v2 status
    """

    ATTR = {
        "branch.oid": "oid",
        "branch.head": "head",
        "branch.upstream": "upstream",
        "branch.ab": "ab",
    }

    def __init__(self):
        self.oid = None
        self._head = None
        self.upstream = None
        self.ahead = 0
        self.behind = 0

    def update(self, line: str):
        try:
            hint, rhs = line.split(maxsplit=1)
            setattr(self, self.ATTR[hint], rhs)
        except ValueError:
            raise ValueError(f"unparsable line {line!r}")
        except KeyError:
            raise ValueError(f"unknown attribute {hint!r}")

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, value: str):
        if value == "(detached)":
            self._head = None
        else:
            self._head = value

    @property
    def ab(self):
        return f"+{self.ahead} -{self.behind}"

    @ab.setter
    def ab(self, line: str):
        match = re.match(r"\+(?P<ahead>\d+) -(?P<behind>\d+)", line)
        if not match:
            raise ValueError(f"unparsable value {line!r}")
        self.ahead = int(match.group("ahead"))
        self.behind = int(match.group("behind"))


class DirectoryParser:

    """ Parse directory information from a porcelain v2 status
    """

    UPDATE_FCT = {
        "1": "update_xstaged",
        "2": "update_xstaged",
        "u": "update_unmerged",
        "?": "update_untracked",
    }

    def __init__(self):
        self.staged = 0
        self.unstaged = 0
        self.unmerged = 0
        self.untracked = 0

    def update(self, line: str):
        try:
            hint, rhs = line.split(maxsplit=1)
            getattr(self, self.UPDATE_FCT[hint])(rhs)
        except ValueError:
            raise ValueError(f"unparsable line {line!r}")
        except KeyError:
            raise ValueError(f"unknown format {hint!r}")

    def update_xstaged(self, line: str):
        match = re.match("^(?P<X>[.MTARCD])(?P<Y>[.MTARCD])", line)
        if not match:
            raise ValueError(f"unparsable value {line!r}")
        if match.group("X") != ".":
            self.staged += 1
        if match.group("Y") != ".":
            self.unstaged += 1

    def update_unmerged(self, line: str):
        self.unmerged += 1

    def update_untracked(self, line: str):
        self.untracked += 1
