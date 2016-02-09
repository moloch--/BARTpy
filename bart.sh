#!/bin/bash

# for use with Bitbar https://github.com/matryer/bitbar

export PATH="/usr/local/bin:/usr/bin:$PATH"
echo "🚈| dropdown=false"
echo "---"

python ~/.bitbar/bart/cli-bart.py --station 24th --no-color
