
#! /bin/bash

# from the secret env folder
# make all filenames keys and their contents values
# the bash command makes something like this
#    export <filename>=`cat <filename>`
# then the find command runs the bash command for each file
# then we source the result.

if [ -d "/var/secret/env" ]; then
    for file in "/var/secret/env"/*
    do
        if [ ! -d "${file}" ] ; then
            export `basename "${file}"`=`cat "${file}"`
        fi
    done
fi

exec "$@"
