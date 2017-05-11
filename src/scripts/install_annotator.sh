#!/bin/bash
# Install required packages
set -e

# install props
echo "Installing PropS..."
wget https://github.com/gabrielStanovsky/props/archive/master.zip -O props.zip
unzip -f props.zip
pushd props-master
python setup.py install
popd

# Install python packages
echo "Installing requirements"
pip install -r ./scripts/requirements.txt

# Install spacy
python -m spacy download en
