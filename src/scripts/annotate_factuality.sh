#!/bin/bash
# Usage:
#  ./annotate_factuality.sh
# Read sentences from STDIN and print factuality parses to STDOUT
set -e
python ./annotate_factuality.py  --truthteller=../truth_teller/ --default=3.0
