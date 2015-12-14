BEGIN {
    RS = ""
    FS = "\n"
    ORS = "\n\n"
    OFS = "\n"
    KS = "::" # key separator
    search = tolower(search)
}
NR == 1 {
    for (i = 1; i <= NF; i++) {
    	if (index($i, ":") == 1)
	    $i = substr($i, 2, length($i) - 1)
	fields[i] = $i
    }
    print
}
NR > 1  {
    for (i = 1; i <= NF; i++) {
	$i = normalize_field(i, $i)
    }
}
NR > 1 && tolower($0) ~ search { print } # only print records that match search

function in_array(item, array) {
    for (k in array) {
	if (array[k] == item)
	    return 1
    }
    return 0
}

function normalize_field(i, val) {
    split(val, parts, KS)
    if (length(parts) > 1) {
	# some light validation
	if (in_array(parts[1], fields) == 0) {
	    printf "Error: undefined field \"%s\"\n", parts[1] > "/dev/stderr"
	    exit 1
	}
    	return parts[1] KS parts[2]
    }
    return fields[i] KS val
}
