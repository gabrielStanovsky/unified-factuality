#!/usr/bin/env python
#coding:utf8
""" Usage:
  props_server --props=PATH_TO_PROPS [--port=PORT]

Run a props instance and answer requests for dependency parsing on the specified port.
The props parameter points to the root directory of PropS.
Port specifies the port on which to run PropS (default: 8081)
"""

from bottle import route, run, get, post, request, response, static_file
import sys
import bottle
import os.path
import codecs
from docopt import docopt
import logging
import requests
logging.basicConfig(level = logging.DEBUG)


PROPS_PORT = 8081

def post_to_props(sent, hostname = 'http://127.0.0.1', port = PROPS_PORT):
    """
    Send a sentence to parse with props
    """
    request_ = '{}:{}/tparse'.format(hostname, port)
    logging.debug(request_)
    return requests.get(request_,
                        params = {'text': sent})


def is_single_word_predicate(node):
    """
    Return true iff the node represents a single-word, non-implicit, predicate
    """
    return node.isPredicate \
        and (len(node.text) == 1) \
        and (not node.is_implicit())

def ent_to_str(ent, default):
    """
    Return a string representation of a single word entry.
    Also replaces the DEFAULT label with the default value
    """
    ent[2] = (ent[2] \
              if ent[2] != Truth_teller_factuality_annotator.DEFAULT \
              else default)
    return '\t'.join(map(str,ent))

def _get_props_predicate_indices(sent):
    """
    Get PropS' predicate indices for a given sentence
    """
    graph = single_sentence_props(sent)
    return  ",".join(map(str,
                         [node.text[0].index - 1
                          for node in graph.nodes()
                          if is_single_word_predicate(node)]))

def single_sentence_props(sent):
    """
    Return a graph representation of a single sentence with PropS
    """
    g,tree = parseSentences(sent, props_path)[0]
    return g

@get('/tparse')
def tparse():
    """
    Expose parsing of PropP, returns a list of PropS predicates.
    """
    sent = request.GET.get('text','').strip()
    logging.debug("Parsing: {}".format(sent))
    return _get_props_predicate_indices(sent)

if __name__ == "__main__":
    args = docopt(__doc__)

    # Parse arguments
    props_path = args["--props"]
    port = 8081 \
           if not (args["--port"]) \
              else int(args["--port"])

    # Init props
    sys.path.insert(0, props_path)
    # After adding the props path we can import its packages and load parsers
    from props.webinterface.log import log
    import props.applications.run
    from props.applications.viz_tree import DepTreeVisualizer
    from props.applications.run import load_berkeley
    from props.applications.run import parseSentences
    from props.applications.run import load_berkeley
    from props.applications.run import parseSentences
    load_berkeley()

    # Check everything's working locally
    logging.debug("Performing a quick sanity check..")
    check_result = _get_props_predicate_indices("John refused to run")
    expected = "1,3"
    assert check_result == expected, "Got: {}; Expected: {}".format(check_result, expected)
    logging.debug("OK!")

    # Start server
    run(host = '',
        port = port)
