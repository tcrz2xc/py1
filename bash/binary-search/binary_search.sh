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
    
    value=$1
    shift
    sorted=$(printf '%s\n' "$@" | sort -n | tr '\n' ' ')
    IFS=' ' read -ra lst <<< "$sorted"
    len=${#lst[@]}
    #check for empty array
    if [[ $len -eq 0 ]]; then
        echo -1
        return
    fi    
    mid=$(( len / 2 ))
    if [[ "${lst[$mid]}" -eq "$value" ]]; then
        echo "$mid"
    elif [[ "${lst[$mid]}" -lt "$value" ]]; then
        local result
        #recursion and inclusion of the offset +1
        result=$(main "$value" "${lst[@]:((mid+1))}") #recursion is runned in a subshell no paranthesis for the arguments needed
        if [[ $result -eq -1 ]]; then
            echo -1
        else
            echo $(( mid + 1 + result))
        fi
    else
        main "$value" "${lst[@]:0:mid}"
    
    fi
        
}

main "$@"
