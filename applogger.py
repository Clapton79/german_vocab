import logging
from os import getenv 

logfile = getenv('VOCAB_LOGFILE', 'app.log')
log_level = getenv('VOCAB_LOG_LEVEL','DEBUG').upper()
log_to_screen = getenv('VOCAB_LOG_TO_SCREEN', False)

def get_log_level_enum(level):
    try:
        return getattr(logging, level)
    except AttributeError:
        return logging.DEBUG

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile)
    fh.setLevel(get_log_level_enum(log_level))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if log_to_screen:
        print("Streaming logs to screen")
        sh = logging.StreamHandler()
        sh.setLevel(get_log_level_enum(log_level))
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    return logger
    
logger = setup_logger()
        
