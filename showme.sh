#!/bin/bash

set -o errexit
set -o nounset

o1="****[ TODO ]****"
o2=$(sh listkeeper.sh -f ~/Dropbox/todo.list -s priority)
o3="****[ PROJECTS ]****"
o4=$(sh listkeeper.sh -f ~/Dropbox/projects.list -s importance -r)
output="$o1\n$o2\n\n$o3\n$o4"

clear

if [ -t 1 ]; then # stdout is a tty
    printf "$output" | less --no-init --quit-if-one-screen --raw-control-chars
else
    printf "$output"
fi
