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
    s=$1   
    case "$s" in
        Alice)
            echo "One for $1, one for me."
             ;;
        Bob)
            echo "One for $1, one for me."
            ;;
        Bohdan)
            echo "One for $1, one for me."
            ;;
        Zaphop)
            echo "One for $1, one for me."
            ;;
        "John Smith")
            echo "One for $1, one for me."
            ;;
        "* ") 
            echo "One for $1, one for me."   
            ;;
        *)
            echo "One for you, one for me."
            ;;
    esac
   }

#   # call main with all of the positional arguments
   main "$@"
