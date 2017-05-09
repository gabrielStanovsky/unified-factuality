#!/bin/bash
python ./split_corpus.py --in=tt_on_factbank/fb+feats\
       --out=tt_on_factbank/ --train=0.68 --dev=0.25
