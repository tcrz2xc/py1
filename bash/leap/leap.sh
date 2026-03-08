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
    year=$1
    re='^[0-9]+$'
    if [[ $# -gt 1 ]]; then
        echo "Usage: leap.sh <year>"
        exit 1
    elif ! [[ $year =~ $re ]]; then
        echo "Usage: leap.sh <year>"
        exit 1
    fi
    if (( year%4==0 )) &&  ! (( year%100==0 )); then
        echo "true"
    elif (( year%100 ==0 )) && (( year%400==0 )); then
        echo "true"
    else
        echo "false"
    fi
}

#   # call main with all of the positional arguments
main "$@"
