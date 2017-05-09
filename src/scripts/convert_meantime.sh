#!/bin/bash
set -e
python ./convert_meantime_to_conll.py --in=../data/meantime/meantime_newsreader_english_oct15/intra_cross-doc_annotation/ --out=../data/meantime/meantime_cross_filtered.conll
