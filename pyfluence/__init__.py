__version__ = "0.1.0"

import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)