""" Usage:
  webserver --truthteller=TRUTHTELLER_PATH [--port=PORT]

Run a factuality server
"""

import cherrypy
from spacy.en import English
from docopt import docopt
from collections import defaultdict
from bratvisualizer.brat_wrapper import conll_to_brat
import requests
import logging
from truth_teller_factuality_annotator import Truth_teller_factuality_annotator
from truth_teller_wrapper import Truth_teller_wrapper
from annotate_factuality import parse_sent

logging.basicConfig(level = logging.DEBUG)

# CONSTANTS
DEFAULT_PORT = 8086  # Default port for this server

class Factuality_server:
    """
    Factuality server instance
    """
    def __init__(self, tt_path):
        """
        Init spacy engine and clear cache
        tt_path - the path to the root of truthteller
        """
        self.tt_annotator = Truth_teller_factuality_annotator(Truth_teller_wrapper(tt_path))

    @cherrypy.expose
    def factcheck(self, **kwargs):
        """
        Run factuality annotation on a single sentence, returns brat representation html
        """
        logging.debug('factcheck args: {}'.format(kwargs))
        sent = kwargs['text']
        output = conll_to_brat(parse_sent(self.tt_annotator, sent.strip()))
        return output

if __name__ == "__main__":
    # Parse args
    args = docopt(__doc__)
    logging.debug(args)
    tt_path = args["--truthteller"]
    port = args['--port']
    if port:
        port = int(port)
    else:
        port = DEFAULT_PORT
        logging.debug("Using default port: {}".format(DEFAULT_PORT))


    # Init server
    server = Factuality_server(tt_path)
    logging.debug("Factcheck loaded")
    cherrypy.config.update({"server.socket_port" : port})
    cherrypy.config.update({"server.socket_host" : "0.0.0.0"})
    cherrypy.quickstart(server)
    logging.debug('running spaCy server on port {}'.format(port))
