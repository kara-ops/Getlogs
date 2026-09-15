import logging
from formatter import JSONFormatter



def setup_logging(level: str = "INFO") -> None:
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return
    root_logger.setLevel(level)
    handler  = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)
    
    

setup_logging()

logger = logging.getLogger("test")
logger.info("user is testing")
logger.error("error testing")
logger.critical("fak this shi")
logger.debug("this shi passes")