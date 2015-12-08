BEGIN {
    RS = ""; FS = "\n"; OFS = "\t"
    nf_req = nf_opt = 0
}
NR == 1 {
    for (i = 1; i <= NF; i++) {
    	if (index($i, ":") > 0) {
    	    $i = substr($i, 2, length($i) - 2);
    	    fields_opt[++nf_opt] = $i;
    	} else {
    	    fields_req[++nf_req] = $i;
    	}
    }
    print
}
NR > 1 {
    for (i = 1; i <= nf_req; i++) { $i = $i }
    for (i = 1; i <= nf_opt; i++) {
    	for (j = 1; j <= NF; j++) {
    	    if (index($j, fields_opt[i])) {
    		val = substr($j, length(fields_opt[i]) + 3)
		$j = ""; $(nf_req + i) = val
    	    }
    	}
    }
    print
}
