#!/bin/bash

set -o errexit
set -o nounset

display_usage() {
    echo "usage: $0 [arguments]"
}

# if less than one argument supplied, display usage
if [ $# -le 0 ]
then
    display_usage
    exit 1
fi

# check whether user had supplied -h or --help . If yes display usage
if [[ ( $# == "--help") || $# == "-h" ]]
then
    display_usage
    exit 0
fi

sed 's/^[[:blank:]]*//g' $1 | awk -f listkeeper.awk # | sort -t't' -k 2 | less -FX
