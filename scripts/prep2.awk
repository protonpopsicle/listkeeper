BEGIN {
    RS = ""
    FS = "\n"
    OFS = "|"
    KS = "::"
    sortCol = 0
}
NR == 1 {
    for (i = 1; i <= NF; i++) {
	fields[i] = $i
	if (tolower(sortField) == tolower($i))
	    sortCol = i
    }
    $1=$1; print
    if (sortField == "")
	sortField = fields[1]
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
    if (sortCol == 0)
	print
    else {
	command = "sort -t'" OFS "' -k " sortCol "," sortCol
	if (reverse == 1)
	    command = command " -r"
	print | command
    }
    for (i in val)
	delete val[i]
}
