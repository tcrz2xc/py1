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
    n=$1
    t=total
    count=0
    if [[ $n == "$t" ]]; then
        echo "2^64 - 1" | bc
    else
        for ((i=0; i< (n-1); i++ )); do 
            count=$((count+2**i))
        done
        if [[ n -lt 1 ]] || [[ n -gt 64 ]]; then
            echo "Error: invalid input"
            exit 1
        elif [[ n -eq 64 ]]; then
            neg=$(( count + 1  ))
            echo ${neg#-}
        
        else
            echo "$(( count + 1 ))"
        fi
    fi
}

main "$@"
