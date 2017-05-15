"""
  Check if props server is up at the default port
"""

from props_server import post_to_props
import logging
logging.basicConfig(level = logging.DEBUG)
post_to_props("John refused to run")
