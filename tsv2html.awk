BEGIN {
    FS = "\t";
    printf "<table>\n"
}
NR == 1 {
    printf "<tr>\n"
    for (i = 1; i <= NF; i++) { printf "<th>%s</th>\n", $i }
    printf "</tr>\n"
}
NR > 1 {
    printf "<tr>\n"
    for (i = 1; i <= NF; i++) { printf "<td>%s</td>\n", $i }
    printf "</tr>\n"
}
END {
    printf "</table>\n"
}
