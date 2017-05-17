#!/bin/bash
# Usage:
#  ./run_props_server.sh
# Run props on the default port
set -e
python ./parsers/props_server.py --props=props/ --port=${1:-8081}
