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

function optional_field_pos(field) {
    pos = -1
    for (i = 1; i <= nf_opt; i++) {
    	if (index(field "::", fields_opt[i])) {
	    pos = i;
	}
    }
    return pos
}

NR > 1 {
    for (i = 1; i <= NF; i++) {
	if (i > nf_req) {
	    field_pos = optional_field_pos($i)
	    printf fmt, field_pos
	} else {
	    printf fmt, $i
	}
    }
    printf "\n"
}
