""" Usage:
    annotate_factuality --truthteller=PATH_TO_TT --props=PATH_TO_PROPS --default=DEFAULT_VALUE

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
    props_path = args["--props"]
    default_val = args["--default"]

    # Initialize TruthTeller
    tt_annotator = Truth_teller_factuality_annotator(Truth_teller_wrapper(tt_path))

    # Initialize PropS
    sys.path.insert(0, props_path)
    # After adding the props path we can import its packages
    from props.applications.run import load_berkeley
    from props.applications.run import parseSentences
    load_berkeley(path_to_berkeley = os.path.join(props_path, 'props/berkeleyparser/'))

    logging.info("Reading sentences from STDIN (hit Ctrl-D to finish)")
    for line in sys.stdin.readlines():
        sent = line.strip()
        logging.info("Parsing: {}".format(sent))
        graph = single_sentence_props(sent)
        predicate_indices = [node.text[0].index - 1
                             for node in graph.nodes()
                             if is_single_word_predicate(node)]
        print ('\n'.join([ent_to_str(list(ent), default_val) for
                          ent in tt_annotator.annotate_sentence(sent, predicate_indices)]))
