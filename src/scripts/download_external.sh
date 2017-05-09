#!/bin/bash
## Downloads the original external resources from the web.
## Stores them in /data/external_annotations
## Run from src: ./scripts/download_external.sh
## This makes use of the gdrive package to download the MEANTIME corpus from Google Drive
set -e

# Preliminary: install GDRIVE
echo "Downloading gdrive"
wget "https://docs.google.com/uc?id=0B3X9GlR6EmbnWksyTEtCM0VfaFE&export=downl" -O ./scripts/gdrive
chmod +x ./scripts/gdrive
echo "SUCCESSFULY DOWNLODED GDRRIVE"

# Download UW
echo "Downloading UW corpus to ../data/external_annotations/uw/ ..."
mkdir -p ../data/external_annotations/uw
wget https://bitbucket.org/kentonl/factuality-data/get/a773e3444e02.zip -O ../data/external_annotations/uw/uw_repo.zip
unzip ../data/external_annotations/uw/uw_repo.zip -d ../data/external_annotations/uw/
mv -v ../data/external_annotations/uw/kentonl-factuality-data-*/* ../data/external_annotations/uw/
rmdir ../data/external_annotations/uw/kentonl-factuality-data-*/
echo "SUCCESSFULY DOWNLOADED UW CORPUS"

# Download MEANTIME
