#!/bin/bash
set -e
MEANTIME_RAW_DIR="../data/external_annotations/meantime/"
MEANTIME_OUTPUT_DIR="../data/unified/meantime"
mkdir -p ${MEANTIME_OUTPUT_DIR}
python ./convert_meantime_to_conll.py --in=${MEANTIME_RAW_DIR}/meantime_newsreader_english_oct15/intra_cross-doc_annotation/ --out=${MEANTIME_OUTPUT_DIR}/meantime_cross_filtered.conll

# Split the file - should produce the same split every time, since we set the seed in split corpus
python ./split_corpus.py --in=${MEANTIME_OUTPUT_DIR}/meantime_cross_filtered.conll\
       --out=${MEANTIME_OUTPUT_DIR} --train=0.68 --dev=0.17
