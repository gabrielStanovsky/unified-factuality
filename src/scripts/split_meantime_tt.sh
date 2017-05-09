#!/bin/bash
python ./split_corpus.py --in=tt_on_meantime/mt+feats\
       --out=tt_on_meantime/ --train=0.68 --dev=0.17
