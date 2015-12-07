BEGIN {
    RS = ""; FS = "\n";
    fmt = "%s\t";
    nf_req = 0;
    nf_opt = 0
}
NR == 1 {
    for (i = 1; i <= NF; i++) {
	if (index($i, ":") > 0) {
	    name = substr($i, 2, length($i) - 2);
	    fields_opt[++nf_opt] = name;
	}
	else {
	    name = $i
	    fields_req[++nf_req] = name;
	}
	printf fmt, name
    }; printf "\n"
}
NR > 1 {
    for (i = 1; i <= nf_req; i++) { printf fmt, $i };
    for (i = 1; i <= nf_opt; i++) {
	found = 0
	for (j = 1; j <= NF; j++) {
	    if (index($j, fields_opt[i])) {
		found = 1; val = substr($j, length(fields_opt[i]) + 3)
		printf fmt, val
	    }
	}
	if (found == 0) {
	    printf fmt, ""
	}
    }; printf "\n"
}
# END { print "total", NR }
