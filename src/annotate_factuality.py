""" Usage:
annotate_factuality --truthteller=PATH_TO_TT --default=DEFAULT_VALUE  --props_hostname=PROPS_HOSTNAME --props_port=PROPS_PORT --spacy_hostname=SPACY_HOSTNAME --spacy_port=SPACY_PORT

Annotate raw sentences from STDIN with factulity and print to STDOUT.

Options:
  truthteller    Path to truthteller root directory
  props          Path to PropS root directory
  default        Default value for annotations.
                 This is the value given for annotations which PropS recognizes as predicate, yet are not available in
                 the TruthTeller lexicon.
                 In news domain, this is probably better to set to factual (+3.0)
"""

from docopt import docopt
import fileinput
import logging
import sys
import os
logging.basicConfig(level = logging.INFO)
from truth_teller_factuality_annotator import Truth_teller_factuality_annotator
from truth_teller_wrapper import Truth_teller_wrapper
from parsers.props_server import post_to_props

def is_single_word_predicate(node):
    """
    Return true iff the node represents a single-word, non-implicit, predicate
    """
    return node.isPredicate \
        and (len(node.text) == 1) \
        and (not node.is_implicit())

def single_sentence_props(sent):
    """
    Return a graph representation of a single sentence with PropS
    """
    g,tree = parseSentences(sent, props_path)[0]
    return g

def ent_to_str(ent, default):
    """
    Return a string representation of a single word entry.
    Also replaces the DEFAULT label with the default value
    """
    ent[2] = (ent[2] \
              if ent[2] != Truth_teller_factuality_annotator.DEFAULT \
              else default)
    return '\t'.join(map(str,ent))

if __name__ == "__main__":
    args = docopt(__doc__)

    # Parse arguments
    tt_path = args["--truthteller"]
    default_val = args["--default"]
    props_hostname = args["--props_hostname"]
    props_port = int(args["--props_port"])
    spacy_hostname = args["--spacy_hostname"]
    spacy_port = int(args["--spacy_port"])

    # Initialize TruthTeller
    tt_annotator = Truth_teller_factuality_annotator(Truth_teller_wrapper(tt_path))

    logging.info("Reading sentences from STDIN (hit Ctrl-D to finish)")
    for line in sys.stdin.readlines():
        sent = line.strip()
        logging.info("Parsing: {}".format(sent))
        predicate_indices = [int(x) 
                             for x in 
                             post_to_props(sent, hostname = props_hostname, port = props_port).text.split(',')
                             if x]
        
        print ('\n'.join([ent_to_str(list(ent), default_val) for
                          ent in tt_annotator.annotate_sentence(sent, predicate_indices, hostname = spacy_hostname, 
                                                                port = spacy_port)]))
