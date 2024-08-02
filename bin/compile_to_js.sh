#!/bin/bash

# if '-f' (force compile), remove the old files before compiling
if [[ " $* " == *" -f "* ]]; then
    rm -rf ./emcommon_js/*
fi
transcrypt --nomin --ecom --xreex ./src/index.py -od ../emcommon_js
