#!/bin/bash
set -e
python ./readers.py --fb_path=../data/factbank_v1/data/annotation/ --out=../data/factbank_v1/factbank_filtered.conll
