#!/bin/sh
set -e
python convert_uw_to_conll.py --in=../data/uw/factuality-data/dev/ --out=../data/uw/factuality-data/dev.conll
python convert_uw_to_conll.py --in=../data/uw/factuality-data/train/ --out=../data/uw/factuality-data/train.conll
python convert_uw_to_conll.py --in=../data/uw/factuality-data/test/ --out=../data/uw/factuality-data/test.conll
