#!/usr/bin/env bash

set -Eeo pipefail

function show_help {
    echo """
    Commands
    ----------------------------------------------------------------------------
    bash              : run bash
    eval              : eval shell command
    start             : start extractor with settings from extractor
    """
}


case "$1" in
    bash )
        bash
    ;;

    eval )
        eval "${@:2}"
    ;;

    start )
        tail -f /dev/null
    ;;
esac