#!/bin/bash
# Usage:
#  stop_server.sh
# Kill the processes of a currently running server

# kill props server
kill `ps -ef | grep props | grep python | awk '{print $2}'`

# kill spacy server
kill `ps -ef | grep spacy | grep python | awk '{print $2}'`
