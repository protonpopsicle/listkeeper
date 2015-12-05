#!/bin/bash

sed 's/^[[:blank:]]*//g' $1 | awk -f listkeeper.awk | less -FX
