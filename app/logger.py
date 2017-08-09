#from controller import application
import os
import logging
import logging.handlers


def create_logger(log_file):
    logger_name = log_file.replace('.', '_')
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s"
                                  " - %(filename)s:%(lineno)d %(funcName)s"
                                  "- %(message)s")
    if not logger.handlers:
        directory = './log/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        handler = logging.handlers.RotatingFileHandler(
            directory + log_file, maxBytes=(1048576 * 10), backupCount=9)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # For logging to stderr
    if 'stream_handler' not in [each.get_name() for each in logger.handlers]:
        stream_handler = logging.StreamHandler()
        stream_handler.set_name('stream_handler')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger