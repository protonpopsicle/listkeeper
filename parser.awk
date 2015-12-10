BEGIN {
    RS = ""; FS = "\n"; fmt = "%s\t"
    nf_req = nf_opt = 0
}
NR == 1 {
    for (i = 1; i <= NF; i++) {
    	if (index($i, ":") == 1) {
	    $i = substr($i, 2, length($i) - 1)
	    fields_opt[++nf_opt] = $i
	} else {
	    fields_req[++nf_req] = $i
	}
	printf fmt, $i
    }
    printf "\n"
}
NR > 1 {
    for (i = 1; i <= NF; i++) {
	if (i <= nf_req)
	    printf fmt, $i
	else {
	    for (j = 1; j <= nf_opt; j++) { # foreach optional field
		if (index($i, fields_opt[j]) == 1)
		    printf fmt, substr($i, length(fields_opt[j]) + 2)
		else
		    printf fmt, ""
	    }
	}
    }
    printf "\n"
}
