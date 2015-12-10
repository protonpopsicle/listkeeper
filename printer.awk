function norm()  { system("tput sgr0") }
function red()   { system("tput setaf 1") }
function green() { system("tput setaf 2") }
function bold() { system("tput bold") }

BEGIN {
    FS = "\t";
    fmt = "%-24.24s  ";
}
{
    for (i = 1; i <= NF; i++) {
	if (NR == 1) {
	    bold()
	    $i = toupper($i)
	} else {
	    norm()
	}
	printf fmt, $i
    }
    printf "\n"
}
