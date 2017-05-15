from factuality_server import Factuality_server as fs
import logging
logging.basicConfig(level = logging.DEBUG)
print fs.post_to_props("John refused to run").text
