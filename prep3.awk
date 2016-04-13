BEGIN {
    FS = "|"
    # KS = "::"
    excludePat = "title"
}
{
    for (i = 1; i <= NF; i++) {
    	if ($i ~ excludePat) {
    	    # printf $i FS
    	} else {
	    printf $i FS
	}
    }
    printf "\n"
}
