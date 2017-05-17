""" Usage:
    truth_teller_wrapper --in=SENTENCE

Run truthteller on a single sentence from python using spacy
Prints output to screen.
"""

from docopt import docopt
import logging
import requests
import subprocess
from operator import itemgetter
logging.basicConfig(level = logging.INFO)

class Truth_teller_wrapper:
    """
    Wrap Truth Teller call to run from python
    """
    def __init__(self, path_to_tt):
        """
        Initialize a truth teller instance from the given path
        """
        self.path_to_tt = path_to_tt

    def annotate(self, sent, hostname, port):
        """
        Run truthteller on a single sentence.
        Returns a list of (word, truth annotation = (sig, nu, ct, pt))
        """
        from parsers.spacy_server import Spacy_server
        # Cache parse in spacy and run truthteller
        cache_response = Spacy_server.post_to_cache(sent, hostname = hostname, port = port)
        assert cache_response.status_code == 200, "error in reponse {}".format(cache_response)
        cache_response = cache_response.text.split('\t')

        tt_output = subprocess.check_output(['./run_truthteller.sh', sent])
        logging.debug(['./run_truthteller.sh', sent])
        logging.debug(tt_output)


        # Read truthteller's output
        tt_output = {}
        for i, line in enumerate(open("{}/annotatedSentences/sentence_1.cnt".format(self.path_to_tt)).readlines()):
            line = line.strip()
            if not line:
                continue
            tt_ind, word, lemma, cpostag, postag, feats, head, dep, _, _, sig, nu, ct, pt = line.split('\t')
            tt_output[int(tt_ind)] = (word, int(head), (sig, nu, ct, pt))

        # Truthteller's output token indexing is messed-up and we need to reconstruct the sentence
        # We assume that a key of word_head_word is unique and identify word (and annotation order) by it
        tt_encoding = {}
        for (ind, vals) in tt_output.iteritems():
            word, head, val = vals
            key = '{}_{}'.format(word, tt_output[head][0] if head else 'ROOT')
            tt_encoding[key] = val

        return [(w.split('_')[0], tt_encoding[w]) for w in cache_response]

if __name__ == '__main__':
    args = docopt(__doc__)
    sent = args["--in"].strip()
    tt_wrapper = Truth_teller_wrapper('../truth_teller')
    annots = tt_wrapper.annotate(sent)
    print('\n'.join(['{}\t{}\t{}'.format(word_ind, w, '\t'.join(annot))
                     for (word_ind, (w, annot)) in enumerate(annots)]))
