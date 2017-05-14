""" Usage:
spacy_server [--port=PORT]

Run a spacy instance and answer requests for dependency parsing on the specified port.
"""

import cherrypy
from spacy.en import English
from docopt import docopt
from collections import defaultdict
import requests
import logging
logging.basicConfig(level = logging.DEBUG)

# CONSTANTS
TT_PORT = 10345  # Default port expected by Truthteller

class Spacy_server:
    """
    Spacy server instance
    """
    def __init__(self):
        """
        Init spacy engine and clear cache
        """
        self.nlp = English()
        self.cached_parses = {}

    def make_key(self, sent):
        """
        Get a key for cache from sent
        """
        return sent.replace(' ','').replace("'","").replace('"','')[:50]

    @staticmethod
    def post_to_cache(sent, hostname = 'http://127.0.0.1', port = TT_PORT):
        """
        Send a sentence to chache at the spacy server running at the given port.
        """
        request_ = '{}:{}/cache'.format(hostname, port)
        logging.debug(request_)
        return requests.post(request_,
                          data={'text': sent})

    @cherrypy.expose
    def cache(self, **kwargs):
        """
        Cache parse result - this is a workaround to ignore truthteller's tokenization.
        Will be called from truthteller wrapper prior to the real truthteller call.
        TODO: check if this doesn't mess with TruthTeller's output.
        """
        logging.debug('Cache args: {}'.format(kwargs))
        sent = kwargs['text']
        toks = self.nlp(sent)
        self.last_toks = toks
        key = self.make_key(sent)
        logging.debug("Cache key: {}".format(key))
        self.cached_parses[key] = toks
        return '\t'.join(['{}_{}'.format(str(tok), str(tok.head) if (tok.head != tok) else "ROOT") for tok in toks])

    @cherrypy.expose
    def parse(self, **kwargs):
        """
        Return a parse request in the tagged_text argument.
        NOTE: This currently ignores the tokenization by looking at the cached result (if exists)
        which was run through spacy's pipeline.
        """
        logging.debug('Parse args: {}'.format(kwargs))
        input_ = kwargs['tagged_text']
        sent = ' '.join([w.split('_')[0] for w in input_.split(' ')])
        logging.info("Parsing: {}".format(sent))

        key = self.make_key(sent)
        if key in self.cached_parses:
            logging.debug("Returning from cached result")
            self.toks = self.cached_parses[self.make_key(sent)]
        else:
            logging.warn("Not in cache! Defaulting to last cached")
            self.toks = self.last_toks
        return '\n'.join([' '.join(map(str,
                           [tok.i + 1, tok, tok.lemma_.lower(), convert_to_old_sd(tok.tag_),
                            convert_to_old_sd(tok.tag_), '_',
                            0 if (tok.i == tok.head.i) else tok.head.i + 1, # Correct root
                            convert_to_old_sd(tok.dep_), '_', '_']))
              for tok in self.toks]) + '\n' + '\n' # Extra nl to resemble easy first


def convert_to_old_sd(dep):
    """
    Convert new Stanford dependencies to old version (both pos and dep).
    For pos conversion, see:
    http://universaldependencies.org/tagset-conversion/en-penn-uposf.html
    TODO: is there a better name for old vs. new?
    TODO: is there a better 3rd party tool for doing this?
    """
    # Differences between new and old tagsets
    conversion = {
        # deps
        "compound": "nn",
        "case": "possessive",
        "attr": "dobj",
        "nummod": "num",
        "acl": "partmod",
        "oprd": "dep", # TODO: is there a better conversion?
        "relcl": "rcmod",
        "intj": "partmod",
        "nmod": "amod",
        "dative": "iobj",
        "meta": "punct", # TODO: is there a better conversion?
        # pos
        "HYPH": ":",
        "NFP": ":",
        "AFX": "JJ",
        "XX": ":", # TODO: is there a better conversion?

    }

    if dep in conversion:
        return conversion[dep]
    # By default return the same dep
    return dep

if __name__ == "__main__":
    args = docopt(__doc__)
    logging.debug(args)
    port = args['--port']
    if port:
        port = int(port)
    else:
        port = TT_PORT
        logging.debug("Using default port: {}".format(TT_PORT))
    server = Spacy_server()
    logging.debug("spacy loaded")
    cherrypy.config.update({"server.socket_port" : port})
    cherrypy.config.update({"server.socket_host" : "0.0.0.0"})
    cherrypy.quickstart(server)
    logging.debug('running spaCy server on port {}'.format(port))
