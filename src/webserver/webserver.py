""" Usage:
  webserver [--port=PORT]

Run a factuality server
"""

import cherrypy
from spacy.en import English
from docopt import docopt
from collections import defaultdict
from bratvisualizer.brat_wrapper import conll_to_brat
import requests
import logging
logging.basicConfig(level = logging.DEBUG)

# CONSTANTS
DEFAULT_PORT = 8086  # Default port for this server

class Factuality_server:
    """
    Factuality server instance
    """
    def __init__(self):
        """
        Init spacy engine and clear cache
        """
        self.nlp = English()
        self.cached_parses = {}

    @cherrypy.expose
    def factcheck(self, **kwargs):
        """
        Run factuality annotation on a single sentence, returns brat representation html
        """
        logging.debug('factcheck args: {}'.format(kwargs))
        sent = kwargs['text']


if __name__ == "__main__":
    args = docopt(__doc__)
    logging.debug(args)
    port = args['--port']
    if port:
        port = int(port)
    else:
        port = DEFAULT_PORT
        logging.debug("Using default port: {}".format(DEFAULT_PORT))
    server = Factuality_server()
    logging.debug("spacy loaded")
    cherrypy.config.update({"server.socket_port" : port})
    cherrypy.config.update({"server.socket_host" : "0.0.0.0"})
    cherrypy.quickstart(server)
    logging.debug('running spaCy server on port {}'.format(port))
