BEGIN {
    RS = "";
    FS = "\n";
    format = "%-36.36s | %-20.20s | %-15.15s | %-10.10s\n"
}
NR == 1 {
    printf format, toupper($1), toupper($2), toupper($3), toupper($4)
    printf format, "---", "---", "---", "---"
}
NR > 1 {
    printf format, $1, $2, $3, $4
}
