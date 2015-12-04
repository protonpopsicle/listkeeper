#!/bin/bash

awk 'BEGIN { RS = ""; FS = "\n"; fmt = "%-36.35s|:%-10.9s:\n" }; { printf fmt, $1, $2, $3 }' books.dat
