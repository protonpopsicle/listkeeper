#!/bin/bash

sed 's/^[[:blank:]]*//g' $1 | awk -f listkeeper.awk | sort -t'|' -k 2 | \
    sed 's/|/  /g' | less -FX
