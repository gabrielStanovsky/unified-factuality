#!/bin/bash
# Install neccessaary packages for converter
set -e
UW_OUTPUT_DIR="../data/unified/uw"
MEANTIME_OUTPUT_DIR="../data/unified/meantime"
FACTBANK_OUTPUT_DIR="../data/unified/factbank_v1"
GLOBAL_OUTPUT_DIR="../data/unified/"

# Install python requirements
pip install -r ./scripts/corpus_requirements.txt
