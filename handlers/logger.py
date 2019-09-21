import logging
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] [%(process)s] %(message)s',
    '%H:%M:%S'
)
ch.setFormatter(formatter)
logger.addHandler(ch)