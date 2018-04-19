from logging import getLogger, Formatter, StreamHandler, INFO


def create_logger():
    logger = getLogger('api')
    stream_handler = StreamHandler()
    formatter = Formatter('[%(levelname)s]\t%(asctime)s\t%(pathname)s:%(lineno)d\t%(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(INFO)

    return logger


logger = create_logger()
