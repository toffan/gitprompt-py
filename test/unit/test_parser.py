import pytest

import gitprompt.parser as module


# {{{ Fixtures
@pytest.fixture
def parser():
    parser = module.PorcelainV2Parser()
    return parser
# }}}


def test_parse(parser):
    """ Parse porcelain info, regular
    """
    porcelain = """
    # branch.oid 90c190e5f3690c2b14aba9e856a5bfe2f412e51d
    # branch.head feat-#3449
    # branch.upstream origin/feat-#3449
    # branch.ab +9 -13
    1 .D N... 100644 100644 000000 b411dc049761a57c68484fc1c3c0a108fba6fc36 b411dc049761a57c68484fc1c3c0a108fba6fc36 CMakeLists.txt
    1 .M N... 100644 100644 100644 2481dec15a728e57366e27722593ae1fdfda61ad 2481dec15a728e57366e27722593ae1fdfda61ad MANIFEST.in
    1 MM N... 100644 100644 100644 6626a9bb1b3304701baddc534b4741196a266fd8 f3f789debd773645afad11fad8f1388bad06b6b7 README.md
    1 D. N... 100644 000000 000000 daa7ff25b6fa2c55d34920e4213b3a3798d65e46 0000000000000000000000000000000000000000 setup.cfg
    1 A. N... 000000 100644 100644 0000000000000000000000000000000000000000 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 setup.py
    2 R. N... 100644 100644 100644 b37cd8b4ef53ba9171fd518eedf71d0eaecabe4e b37cd8b4ef53ba9171fd518eedf71d0eaecabe4e R100 src/main.cpp	sources/main.cpp
    2 R. N... 100644 100644 100644 0f9d26c5401103904582b941c74781910cc28775 0f9d26c5401103904582b941c74781910cc28775 R100 src/tracer.cpp    sources/trace.cpp
    u UU N... 100644 100644 100644 100644 87a0d1ca910de02c1942d4fae7a8e8955f1c42b0 e030d511f227ffc18d3986333c286ca503f3b9a5 4adae36dff51f64eb7889a2959d56bc087fdbccf test/CMakeLists.txt
    ? .gitignore
    ? CONTRIBUTING.md
    """

    parser.parse(porcelain)

    assert parser.branch.oid == "90c190e5f3690c2b14aba9e856a5bfe2f412e51d"
    assert parser.branch.head == "feat-#3449"
    assert parser.branch.upstream == "origin/feat-#3449"
    assert parser.branch.ahead == 9
    assert parser.branch.behind == 13

    assert parser.directory.staged == 5
    assert parser.directory.unstaged == 3
    assert parser.directory.unmerged == 1
    assert parser.directory.untracked == 2


@pytest.mark.parametrize("line", [
        "# whatever xxxx",
        "# branch.whatever xxxx",
        "# branch.ab +abc -4",
        "# branch.ab -0",
        "# branch.ab +2-3",
        "xyzzy ...",
        "1 XA N... ...",
        "1 DY N... ...",
        "2 .Y N... ...",
        "2 X. N... ...",
    ])
def test_exceptions(parser, line):
    """ Parse porcelain info, parsing errors
    """
    with pytest.raises(ValueError):
        parser.parse(line)
