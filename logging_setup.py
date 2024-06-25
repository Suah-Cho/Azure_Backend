import logging
import logging.handlers
import time


class LoggerSetup:
    def __init__(self) -> None:
        self.logger = logging.getLogger('')
        self.setup_logger()

    def setup_logging(self):
        # add log format
        LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        # configure formatter for logger
        formatter = logging.Formatter(LOG_FORMAT)

        # configure console handler
        console = logging.StreamHandler()
        console.setFormatter(formatter)

        # configure TimeRotatingFileHandler
        log_file = "logs/fastapi-server.log"
        file = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
        file.setFormatter(formatter)

        # add handlers
        self.logger.addHandler(console)
        self.logger.addHandler(file)
