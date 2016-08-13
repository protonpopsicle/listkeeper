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
outFormat=
sortField=
reverseSort=0
search=
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
	-o | --output)
	    shift
	    outFormat=$1
	    ;;
	-r | --reverse)
	    reverseSort=1
	    ;;
	-s | --sort)
	    shift
	    sortField=$1
	    ;;
	-g | --grep)
	    shift
	    search=$1
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

pipeSep=$(sed 's/^[[:blank:]]*//g' $filename | \
		 awk -v search="$search" -f prep1.awk | \
		 awk -v sortField="$sortField" -v reverse=$reverseSort -f prep2.awk)
output=$pipeSep

case "$outFormat" in
    "html")
	output=$(echo "$output" | awk -f html.awk)
	;;
    "raw")
	# do nothing
	;;
    *)
	output=$(echo "$output" | awk -f form.awk)
	;;
esac

if [ -t 1 ]; then # stdout is a tty
    echo "$output" | less --no-init --quit-if-one-screen --raw-control-chars
else
    echo "$output"
fi

# consider the following
# ./listkeeper.sh -f ~/Dropbox/books.list -o raw | awk 'BEGIN {FS = "|"; OFS = "|"}{$1 = ""; $3 = ""; print}'
