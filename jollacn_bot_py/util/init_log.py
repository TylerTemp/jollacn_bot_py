import logging
import sys
import colorlog


def _getlogger(hdlr, logger=None, level=None, color=True):
    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger(logger)
    if color:
        fmt_str = (
            '%(log_color)s'
            '[%(levelname)1.1s %(lineno)3d %(asctime)s %(module)s:%(funcName)s]'
            '%(reset)s'
            ' %(message)s'
        )
    else:
        fmt_str = (
            '[%(levelname)1.1s %(lineno)3d %(asctime)s %(module)s:%(funcName)s]'
            ' %(message)s'
        )
    hdlr.setFormatter(
        colorlog.ColoredFormatter(fmt_str)
    )
    logger.addHandler(hdlr)
    if level is not None:
        logger.setLevel(level)
    return logger


def stdoutlogger(logger=None, level=None, color=True):
    hdlr = logging.StreamHandler(sys.stdout)
    return _getlogger(hdlr, logger, level, color)


def stderrlogger(logger=None, level=None, color=True):
    hdlr = logging.StreamHandler(sys.stderr)
    return _getlogger(hdlr, logger, level, color)


def filelogger(file, logger=None, level=None):
    hdlr = logging.FileHandler(file)
    return _getlogger(hdlr, logger, level, False)


def streamlogger(stream, logger=None, level=None, color=True):
    hdlr = logging.StreamHandler(stream)
    return _getlogger(hdlr, logger, level, color)


getlogger = stdoutlogger


if __name__ == '__main__':
    from logging import DEBUG
    logger = getlogger('test1', DEBUG)
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    logger = getlogger('test2', DEBUG, False)
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
