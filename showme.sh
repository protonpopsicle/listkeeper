#!/bin/bash

set -o errexit
set -o nounset

currentYear=$(date +'%Y')

## Print horizontal ruler with message
rulem ()  {
    # Fill line with ruler character (default "-"), reset cursor, move 2 cols right, print message
    printf -v _hr "%*s" $(tput cols) && echo -en ${_hr// /${2--}} && echo -e "\r\033[2C$1"
}

tput clear
tput setaf 7; rulem '=[ BEGIN ]='
tput setaf 4; printf "$(sh listkeeper.sh -f ~/Dropbox/todo.list -s priority)\n\n"
tput setaf 3; printf "$(sh listkeeper.sh -f ~/Dropbox/projects.list -s importance -r)\n\n"
tput setaf 5; printf "$(sh listkeeper.sh -f ~/Dropbox/resolutions$currentYear.list)\n\n"
tput setaf 7; rulem '=[ END ]='
tput sgr0
