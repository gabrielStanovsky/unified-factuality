#!/bin/bash
# Usage:
#  ./annotate_factuality.sh [PROPS_HOSTNAME PROPS_PORT SPACY_HOSTNAME SPACY_PORT]
# Read sentences from STDIN and print factuality parses to STDOUT
set -e
python ./annotate_factuality.py  --truthteller=../truth_teller/ --default=3.0\
 --props_hostname=${1:-http://127.0.0.1} --props_port=${2:-8081} --spacy_hostname=${3:-http://127.0.0.1} --spacy_port=${4:-10345}
