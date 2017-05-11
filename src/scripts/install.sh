#!/bin/bash
## Main driver for installing, downloading and converting all the needed resources
set -e

# Install prerequisites
./scripts/install_annotator.sh

# Download external resources
./scripts/download_external_corpora.sh

# Convert raw annotations
./scripts/convert_corpora.sh
