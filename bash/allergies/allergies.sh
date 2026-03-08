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
    declare -A allergens
    allergens[1]='eggs'
    allergens[2]='peanuts'
    allergens[4]='shellfish'
    allergens[8]='strawberries'
    allergens[16]='tomatoes'
    allergens[32]='chocolate'
    allergens[64]='pollen'
    allergens[128]='cats'

    s=$(($1 % 256))
    t=$2
    allergen_check=$3
    l="list"
    allen=()

    
    for i in {0..7}; do
        pow_2=$((2**i)) #not a cumulative sum but instead testing bit set to a power of 2
        if ((s & pow_2 )); then
            allen+=("${allergens[$pow_2]}")
        fi
    done
    if [[ "$t" == "$l" ]]; then
        echo "${allen[@]}"
    elif [[ "$t" == "allergic_to" ]]; then
        for allergen in "${allen[@]}"; do
            if [[ "$allergen" == "$allergen_check" ]]; then
                echo true
                return
            fi
        done
        echo false
    fi
    }

#   # call main with all of the positional arguments
main "$@"

