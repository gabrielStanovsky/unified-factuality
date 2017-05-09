#!/bin/bash
## Downloads the original external resources from the web.
## Stores them in /data/external_annotations
## Run from src: ./scripts/download_external.sh
## This makes use of the gdrive package to download the MEANTIME corpus from Google Drive
## NOTE: This will delete and replace all files in the ,./data/external_annotations/
set -e

# Download UW
echo "Downloading UW corpus to ../data/external_annotations/uw/ ..."
rm -fr ../data/external_annotations/uw
mkdir -p ../data/external_annotations/uw
wget https://bitbucket.org/kentonl/factuality-data/get/a773e3444e02.zip -O ../data/external_annotations/uw/uw_repo.zip
unzip ../data/external_annotations/uw/uw_repo.zip -d ../data/external_annotations/uw/
mv -vf ../data/external_annotations/uw/kentonl-factuality-data-*/* ../data/external_annotations/uw/
rmdir ../data/external_annotations/uw/kentonl-factuality-data-*/
echo "SUCCESSFULY DOWNLOADED UW CORPUS"

# Download MEANTIME
echo "Downloading UW corpus to ../data/external_annotations/meantime/ ..."
rm -fr ../data/external_annotations/meantime
mkdir -p ../data/external_annotations/meantime
# Download meantime_newsreader_english_oct15.zip
./scripts/gdrive download 0B1PMaGyhp9maeDY1U1p1N01HcjA --path ../data/external_annotations/meantime/
# Download meantime_newsreader_english_raw_NAF.zip
./scripts/gdrive download 0B1PMaGyhp9maQmlZRWhtQTZ3WjA --path ../data/external_annotations/meantime/
# unzip
unzip ../data/external_annotations/meantime/meantime_newsreader_english_oct15.zip -d ../data/external_annotations/meantime/
unzip ../data/external_annotations/meantime/meantime_newsreader_english_raw_NAF.zip -d ../data/external_annotations/meantime/

#DONE
echo "SUCCESSFULY DOWNLOADED ALL CORPORA"
