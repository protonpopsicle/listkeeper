BEGIN {
    FS = "\t";
    fmt = "%-20.20s  ";
}

{
    for (i = 1; i <= NF; i++) {
	printf fmt, $i
    }
    printf "\n"
}
