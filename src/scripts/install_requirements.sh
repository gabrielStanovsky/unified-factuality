#!/bin/bash
# Install required packages
set -e

# Install python packages
pip install -r ./scripts/requirements.txt

# Install spacy
python -m spacy download en

# install GDRIVE
echo "Downloading gdrive"
wget "https://docs.google.com/uc?id=0B3X9GlR6EmbnWksyTEtCM0VfaFE&export=downl" -O ./scripts/gdrive
chmod +x ./scripts/gdrive
echo "SUCCESSFULY DOWNLODED GDrive"
