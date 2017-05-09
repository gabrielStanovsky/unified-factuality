#!/bin/bash
# Convert downloaded annotations to a unified factuality representation
set -e

echo "Converting UW.."
./scripts/convert_uw.sh

echo "Converting MEANTIME.."
./scripts/convert_meantime.sh


echo "Done with conversion"
