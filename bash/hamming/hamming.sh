#!/usr/bin/env bash

# The following comments should help you get started:
# - Bash is flexible. You may use functions or write a "raw" script.
#
# - Complex code can be made easier to read by breaking it up
#   into functions, however this is sometimes overkill in bash.
#
# - You can find links about good style and other resources
#   for Bash in './README.md'. It came with this exercise.
#
#   Example:
#   # other functions here
#   # ...
#   # ...
#
main () {
    s=("$1")
    a=("$2")
    lens=${#s}
    lena=${#a}
    count=0
    if (($#<2)); then
        echo "Usage: hamming.sh <string1> <string2>"
        exit 1
    elif ((lens==0)) && ((lena>0)); then
        echo "strands must be of equal length"
        exit 1
    elif ((lens>0)) && ((lena==0)); then
        echo "strands must be of equal length"
        exit 1
    elif ! [[ lens -eq lena ]]; then
        echo "strands must be of equal length"
        exit 1
    fi
    for ((i=0; i<lens; i++)); do
        [[ "${s:$i:1}" == "${a:$i:1}" ]] && ((count++))
        
    done
    total=$((lens-count))
    echo "$total"
}
#
#   # call main with all of the positional arguments
main "$@"

