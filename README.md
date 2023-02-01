# GitPrompt

*Summarize the status of the current git working tree in the prompt. Python
version.*


## Installation

Clone this repository and grant read permission.

### Dependencies

- python >= 3.11.0
- zsh

### Usage

Source *sh/zsh.sh* from your interactive shell initialisation script (usually
*$ZDOTDIR/.zshrc*). Then, use `$(gitprompt_status)` in your prompt (example
below).

Customize the status with the `GITPROMPT_THEME_*` variables.

```zsh
# symlink to ~/.local/lib/gitprompt-py/sh/zsh.sh
source gitprompt-zsh.sh

# Display untracked files count in yellow and preceded by an angle bracket
GITPROMPT_THEME_UNTRACKED="%{$fg[yellow]%}>"

# Setup prompt
PROMPT='%~ $(gitprompt_status)%# '
```

You may dynamically disable *gitprompt* with `unset GITPROMPT_ENABLED`.

## About

This script is undeniably inspired by
[olivierverdier/zsh-git-prompt](https://github.com/olivierverdier/zsh-git-prompt)
with some tweaks:
- only call `git status` once;
- parse, interpret and print all in python;
- simple heuristic for refreshing;
- done by myself :).
