#!/bin/bash
# Convert downloaded annotations to a unified factuality representation
set -e
UW_OUTPUT_DIR="../data/unified/uw"
MEANTIME_OUTPUT_DIR="../data/unified/meantime"
FACTBANK_OUTPUT_DIR="../data/unified/factbank_v1"
GLOBAL_OUTPUT_DIR="../data/unified/"

# Install python requirements
pip install -r ./scripts/corpus_requirements.txt
# Install spacy
python -c "from spacy import __main__; __main__.cli_download('en')"
#python -m spacy download en


# Convert all raw annotations
echo "Converting UW.."
./scripts/convert_uw.sh

echo "Converting MEANTIME.."
./scripts/convert_meantime.sh

echo "Converting FactBank.."
./scripts/convert_factbank.sh

# Create global dev, train, test
echo "Concatenating to global train / dev / test in $GLOBAL_OUTPUT_DIR"
cat $UW_OUTPUT_DIR/dev.conll $MEANTIME_OUTPUT_DIR/dev.conll $FACTBANK_OUTPUT_DIR/dev.conll >\
    $GLOBAL_OUTPUT_DIR/dev.conll

cat $UW_OUTPUT_DIR/train.conll $MEANTIME_OUTPUT_DIR/train.conll $FACTBANK_OUTPUT_DIR/train.conll >\
    $GLOBAL_OUTPUT_DIR/train.conll

cat $UW_OUTPUT_DIR/test.conll $MEANTIME_OUTPUT_DIR/test.conll $FACTBANK_OUTPUT_DIR/test.conll >\
    $GLOBAL_OUTPUT_DIR/test.conll

echo "Done with conversion"
