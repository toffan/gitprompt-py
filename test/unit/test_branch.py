import pytest

import gitprompt.parser as module


# {{{ Fixtures
@pytest.fixture
def branch():
    br = module.Branch()
    return br
# }}}


def test_parse(branch):
    """ Parse porcelain info, regular
    """
    porcelain = """
    # branch.oid 90c190e5f3690c2b14aba9e856a5bfe2f412e51d
    # branch.head feat-#3449
    # branch.upstream origin/feat-#3449
    # branch.ab +9 -13
    ? random stuff at the end
    """

    branch.parse(porcelain)

    assert branch.oid == "90c190e5f3690c2b14aba9e856a5bfe2f412e51d"
    assert branch.head == "feat-#3449"
    assert branch.upstream == "origin/feat-#3449"
    assert branch.ahead == 9
    assert branch.behind == 13


@pytest.mark.parametrize("line", [
        "whatever xxxx",
        "branch.whatever xxxx",
        "branch.ab +abc -4",
        "branch.ab -0",
        "branch.ab +2-3",
        "# branch.upstream origin/feat-#3449",  # leading "# "
    ])
def test_exceptions(branch, line):
    """ Parse porcelain info, parsing errors
    """
    with pytest.raises(ValueError):
        branch.update(line)
