BEGIN {
    FS = "|"
}
NR == 1 { for (i = 1; i<= NF; i++) { $i = toupper($i) } }
{
    for (i = 1; i <= NF; i++) {
	if (length($i) > maxes[i])
	    maxes[i] = length($i)
        fields[NR,i] = $i
    }
}
END {
    for (i = 1; i <= NR; i++) {
    	for (j = 1; j <= length(maxes); j++) {
	    field = fields[i,j]
    	    printf build_fmt_str(maxes[j], field), field
    	}
    	printf "\n"
    }
}

function build_fmt_str(max_len, field) {
    if (max_len >= 38)
	max_len = 38
    isnum = match(field, /^[$]?[-]?[0-9|.]+$/)
    max_part = sprintf("%s.%s", max_len, max_len)
    # if (isnum)
    # 	return "%" max_part "s  "
    return "%-" max_part "s  "
}
