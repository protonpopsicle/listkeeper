#!/bin/bash

set -o errexit
set -o nounset

display_usage() {
    echo "usage: $0 file [arguments]"
}

# if less than one argument supplied, display usage
if [ "$#" -lt 1 ]; then
    display_usage
    exit 1
fi

rawOutput=false
filename=$1
shift

while [ "$#" -gt 0 ]; do
    case $1 in
	-r | --raw)
	    rawOutput=true
	    ;;
	-h | --help)
	    display_usage
	    exit
	    ;;
       	* )
	    display_usage
	    exit
    esac
    shift
done

sed 's/^[[:blank:]]*//g' $filename | \
    awk -f listkeeper.awk # | sort -t't' -k 2 | less -FX
