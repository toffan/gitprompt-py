#!/bin/zsh


__GITPROMPT_DIR=${0:A:h:h:h}


source $__GITPROMPT_DIR/sh/zsh.sh
PROMPT="%{$fg_bold[white]%}%~%{$reset_color%} "'$(gitprompt_status)'"%# "
