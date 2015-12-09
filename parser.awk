BEGIN {
    RS = ""; FS = "\n"; fmt = "%s\t"
    nf_req = nf_opt = 0
}
NR == 1 {
    for (i = 1; i <= NF; i++) {
    	if (index($i, ":") == 1) {
	    $i = substr($i, 2, length($i) - 2)
	    fields_opt[++nf_opt] = $i
	} else {
	    fields_req[++nf_req] = $i
	}
	printf fmt, $i
    }
    printf "\n"
}
NR > 1 {
    for (i = 1; i <= nf_req; i++) { printf fmt, $i }
    for (i = 1; i <= nf_opt; i++) {
    	for (j = 1; j <= NF; j++) {
    	    if (index($j "::", fields_opt[i])) {
		printf fmt, "found"
    		# $(nf_req + i) = $j; $j = ""
    	    }
    	}
    }
    printf "\n"
}
