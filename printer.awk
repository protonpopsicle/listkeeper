function build_fmt_str(max_len) {
    if (max_len >= 38)
	max_len = 38
    return "%-" sprintf("%s.%s", max_len, max_len) "s  "
}

BEGIN {
    FS = "\t";
    nrows = 0
}
{
    for (i = 1; i <= NF; i++) {
	if (length($i) > maxes[i])
	    maxes[i] = length($i)
        fields[NR,i] = $i
    }
    nrows++
}
END {
    for (i = 1; i <= nrows; i++) {
    	for (j = 1; j <= length(maxes); j++) {
    	    printf build_fmt_str(maxes[j]), fields[i,j]
    	}
    	printf "\n"
    }
}
