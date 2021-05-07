## Simple base logging for Mecha Karen - Base branch from __logging__
## Used for commands and stuff like that

import logging
from .Utils import Enviroment

env = Enviroment()
log_path = '../logs'

global logger

logger = logging.getLogger(__name__)

def update_logger(new_logger: logging.Logger) -> logging.Logger:
    global logger
    
    logger = new_logger
    return logger
    
class Logging:
    def __init__(self, logger_: logging.Logger = None) -> None:
        self.logger = logger_ or logger
        self.file_path = log_path
   
    def update_logger(self, logger_: logging.Logger = None) -> logging.Logger:
        if not logger_:
            logger = logging.getLogger(__name__)
        update_logger(logger)
        self.logger = logger
        return logger
