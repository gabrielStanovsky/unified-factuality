""" Usage:
    factuality_shell --truthteller=PATH_TO_TT --props=PATH_TO_PROPS

Annotate raw sentences from STDIN with factulity and print to STDOUT
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
    Return true iff the nodes represents a single word predicate
    """
    return node.isPredicate and (node.minIndex() == node.maxIndex())

def single_sentence_props(sent):
    """
    Return a graph representation of a single sentence with PropS
    """
    g,tree = parseSentences(sent, props_path)[0]
    return g


if __name__ == "__main__":
    args = docopt(__doc__)

    # Parse arguments
    tt_path = args["--truthteller"]
    props_path = args["--props"]

    # Initialize TruthTeller
    tt_annotator = Truth_teller_factuality_annotator(Truth_teller_wrapper(tt_path))

    # Initialize PropS
    sys.path.insert(0, props_path)
    # After adding the props path we can import its packages
    from props.applications.run import load_berkeley
    from props.applications.run import parseSentences
    load_berkeley(path_to_berkeley = os.path.join(props_path, 'props/berkeleyparser/'))

    # for line in ["John ran home"]: #sys.stdin.readlines():
    #      sent = line.strip()

    # predicate_indices = [node.minIndex() - 1
    #                      for node in g.nodes()
    #                      if is_single_word_predicate(node)]

    # print predicate_indices

    for line in ["Don was dishonest when he said he paid his taxes "]: #sys.stdin.readlines():
        sent = line.strip()
        graph = single_sentence_props(sent)
        predicate_indices = [node.minIndex() - 1
                             for node in graph.nodes()
                             if is_single_word_predicate(node)]
        print tt_annotator.annotate_sentence(sent, predicate_indices)
