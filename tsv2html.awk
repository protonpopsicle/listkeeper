BEGIN {
    FS = "\t";
    print "<!DOCTYPE html>"
    print "<html>"
    print "  <head>"
    print "    <meta charset=\"utf-8\">"
    print "  </head>"
    print "  <body>"
    print "    <table>"
}
NR == 1 {
    tag = "th";
    print "      <thead>"
}
NR == 2 {
    print "      </thead>"
    print "      <tbody>"
}
NR > 1 { tag = "td" }
{
    print "        <tr>"
    for (i = 1; i <= NF; i++) {
	printf "          <%s>%s</%s>\n", tag, $i, tag
    }
    print "        </tr>"
}
END {
    print "      </tbody>"
    print "    </table>"
    print "  </body>"
    print "</html>"
}
