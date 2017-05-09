#!/bin/bash
## Main driver for installing, downloading and converting all the needed resources
set -e

# Install prerequisites
./scripts/install_requirements.sh

# Download external resources
./scripts/download_external.sh

# Convert raw annotations
./scripts/convert.sh
