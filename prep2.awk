BEGIN {
    RS = ""
    FS = "\n"
    OFS = "|"
    KS = "::"
    sort_field = ""
}
NR == 1 {
    for (i = 1; i <= NF; i++) {
	fields[i] = $i
    }
    $1=$1; print
    if (sort_field == "")
	sort_field = fields[1]
}
NR > 1 {
    for (i = 1; i <= NF; i++) {
	split($i, f, KS)
	val[f[1]] = f[2]
    }
    for (i = 1; i <= length(fields); i++) {
    	if (fields[i] in val)
    	    $i = val[fields[i]]
    	else
    	    $i = ""
    }
    print
    for (i in val)
	delete val[i]
}
