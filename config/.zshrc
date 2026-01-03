# Path to your oh-my-zsh installation.
export ZSH="/root/.oh-my-zsh"

ZSH_THEME="fino"
plugins=(git docker)
source $ZSH/oh-my-zsh.sh

# ENV vars
export GOROOT=/usr/lib/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH

# Aliases
alias ll='ls -la'
alias nmap='nmap --reason'
alias proxychains='proxychains4'
