#!/bin/bash
set -e
FACTBANK_RAW_DIR="../data/external_annotations/factbank_v1/"
FACTBANK_OUTPUT_DIR="../data/unified/factbank_v1"
mkdir -p ${FACTBANK_OUTPUT_DIR}
python ./readers.py --fb_path=${FACTBANK_RAW_DIR}/data/annotation/\
       --out=${FACTBANK_OUTPUT_DIR}/factbank_filtered.conll
python  ./split_corpus.py --in=${FACTBANK_OUTPUT_DIR}/factbank_filtered.conll\
        --out=${FACTBANK_OUTPUT_DIR} --train=0.68 --dev=0.25
