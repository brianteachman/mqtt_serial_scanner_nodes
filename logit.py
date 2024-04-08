import logging


HANDLER = logging.FileHandler('C:\\bin\\serial_controller\\data\\service.log')
FORMATTER = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
HANDLER.setFormatter(FORMATTER)


def get_logger(name, debug=False):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO if debug else logging.WARNING)
    log.addHandler(HANDLER)
    return log