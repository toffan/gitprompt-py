import re


def clean(text: str):
    stripped = (line.strip() for line in text.splitlines())
    return [line for line in stripped if line]


class Branch:

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
        self.head = None
        self.upstream = None
        self.ahead = 0
        self.behind = 0

    def parse(self, porcelain: str):
        for line in clean(porcelain):
            if line.startswith("# "):
                self.update(line[2:].strip())

    def update(self, line: str):
        try:
            hint, rhs = line.split(maxsplit=1)
            setattr(self, self.ATTR[hint], rhs)
        except ValueError:
            raise ValueError(f"unparsable line {line!r}")
        except KeyError:
            raise ValueError(f"unknown attribute {hint!r}")

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
