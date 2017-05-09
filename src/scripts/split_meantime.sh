#!/bin/bash
python ./split_corpus.py --in=../data/meantime/meantime_cross_filtered.conll\
       --out=../data/meantime/ --train=0.68 --dev=0.17
