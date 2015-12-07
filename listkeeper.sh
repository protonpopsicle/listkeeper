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

version="0.1.0"
rawOutput=false
filename=

while [ "$#" -gt 0 ]; do
    case $1 in
	-f | --file)
	    shift
	    if [ ! -f $1 ]; then
                echo "File not found!"
		exit 1
	    fi
	    filename=$1
	    ;;
	-r | --raw)
	    rawOutput=true
	    ;;
	-h | --help)
	    display_usage
	    exit
	    ;;
	-v | --version)
	    echo "$version"
	    exit
	    ;;
       	* )
	    display_usage
	    exit
    esac
    shift
done

tsv=$(sed 's/^[[:blank:]]*//g' $filename | awk -f parser.awk)
header=$(echo "$tsv" | head -n 1)
body=$(echo "$tsv" | tail -n +2)
sorted=$(echo "$header" && echo "$body" | sort -t't')
output=$sorted

if [ "$rawOutput" == false ]; then
    output=$(echo "$sorted" | awk -f printer.awk)
fi

if [ -t 1 ]; then # stdout is a tty
    echo "$output" | less --no-init --quit-if-one-screen --raw-control-chars
else
    echo "$output"
fi
