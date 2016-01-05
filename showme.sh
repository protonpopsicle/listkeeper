#!/bin/bash

set -o errexit
set -o nounset

# WIDTH=$(tput cols)

## Print horizontal ruler with message
rulem ()  {
    # Fill line with ruler character (default "-"), reset cursor, move 2 cols right, print message
    printf -v _hr "%*s" $(tput cols) && echo -en ${_hr// /${2--}} && echo -e "\r\033[2C$1"
}

tput clear
# tput setb 4
tput setaf 3
tput bold
rulem '[ TODO ]'
tput sgr0
tput setaf 4
printf "$(sh listkeeper.sh -f ~/Dropbox/todo.list -s priority)\n"
tput setaf 5
tput bold
rulem '[ PROJECTS ]'
tput setaf 6
tput sgr0
printf "$(sh listkeeper.sh -f ~/Dropbox/projects.list -s importance -r)\n"
printf "\n"
