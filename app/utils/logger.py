import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    global logger
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()