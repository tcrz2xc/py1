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

    s=("$@")
    len=${#s}
    sum=0
    for ((i=0; i<len; i++)); do
        c=${s:i:1}
        sum=$((sum + c ** len))
    done
    if [[ $sum == "$*" ]]; then
        echo "true"
    else
        echo "false"
    fi
#      your main function code here
}
#
#   # call main with all of the positional arguments
main "$@"


