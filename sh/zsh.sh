# To install, source this file from your .zshrc file
# and use the gitprompt_status function


__GITPROMPT_DIR=${0:A:h:h}


# Initialize colors.
autoload -U colors
colors

# Allow for functions in the prompt.
setopt PROMPT_SUBST

# Setup hooks for status refresh.
autoload -U add-zsh-hook

add-zsh-hook chpwd gitprompt_hook_chpwd
add-zsh-hook preexec gitprompt_hook_preexec
add-zsh-hook precmd gitprompt_hook_precmd

gitprompt_hook_chpwd() {
    __GITPROMPT_UPDATE=1
}

gitprompt_hook_preexec() {
    case "$2" in
        # Whitelist of common commands that do not to modify the current
        # worktree when used by a benevolent user. As a result, do not update
        # git status after them.
        "ls "*|"tree "*|"cat "*|"less "*|"wc "*|"grep "*|"ag "*|"rg "*|"man "*|"mkdir "*) ;;
        *) __GITPROMPT_UPDATE=1;;
    esac
}

gitprompt_hook_precmd() {
    if [[ $__GITPROMPT_UPDATE == 1 ]]; then
        gitprompt_update
        unset __GITPROMPT_UPDATE
    fi
}

gitprompt_update() {
    if [[ $GITPROMPT_ENABLED != 1 ]]; then
        __GITPROMPT_CURRENT_STATUS=""
    else
        __GITPROMPT_CURRENT_STATUS=$(PYTHONPATH=${PYTHONPATH:+$PYTHONPATH:}$__GITPROMPT_DIR python -P -m gitprompt)
    fi
}

gitprompt_status() {
    echo $__GITPROMPT_CURRENT_STATUS
}


# Default values for the appearance of the prompt. Configure at will.
export GITPROMPT_THEME_PREFIX="["
export GITPROMPT_THEME_SUFFIX="] "
export GITPROMPT_THEME_SEPARATOR=" - "

export GITPROMPT_THEME_BRANCH="%{$fg[blue]%}"
export GITPROMPT_THEME_BEHIND=" %{$fg[blue]%}-"
export GITPROMPT_THEME_AHEAD=" %{$fg[blue]%}+"

export GITPROMPT_THEME_CONFLICTS="%{$fg[red]%}✘"
export GITPROMPT_THEME_UNTRACKED="%{$fg[red]%}?"
export GITPROMPT_THEME_CHANGED="%{$fg[red]%}!"
export GITPROMPT_THEME_STAGED="%{$fg[cyan]%}✔"
export GITPROMPT_THEME_CLEAN="%{$fg_bold[green]%}✔%{$reset_color%}"

export GITPROMPT_ENABLED=1
