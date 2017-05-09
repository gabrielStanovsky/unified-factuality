#!/bin/sh
set -e
UW_RAW_DIR="../data/external_annotations/uw/"
UW_OUTPUT_DIR="../data/unified/uw"
mkdir -p ${UW_OUTPUT_DIR}
python convert_uw_to_conll.py --in=${UW_RAW_DIR}/dev/ --out=${UW_OUTPUT_DIR}/dev.conll
python convert_uw_to_conll.py --in=${UW_RAW_DIR}/train/ --out=${UW_OUTPUT_DIR}/train.conll
python convert_uw_to_conll.py --in=${UW_RAW_DIR}/test/ --out=${UW_OUTPUT_DIR}/test.conll
