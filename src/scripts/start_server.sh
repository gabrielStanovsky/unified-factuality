#!/bin/sh
# Usage:
#  run_server.sh
# Start a spacy and PropS servers on their default ports
set -e
PROPS_PORT=8081
SPACY_SERVER=10345
python ./parsers/props_server.py --props=props/ &
while ! python ./parsers/test_props.py &> /dev/null; do sleep 10; done

#python ./parsers/spacy_server.py &
#sleep 15

echo ""
echo "Server up"
