#!/usr/bin/env python3
import os
import json
import logging
from jollacn_bot_py.doc import parse, __doc__
from jollacn_bot_py.util import init_log
from jollacn_bot_py.util.path import PROJECT_PATH
from jollacn_bot_py.util.mini_six import open
from jollacn_bot_py.twitter.rpc import rpc as twitter_fetcher


def main():
    project_logger = logging.getLogger('jollacn_bot_py')
    project_logger.setLevel(logging.DEBUG)
    init_log.stderrlogger(project_logger)
    del project_logger

    logger = logging.getLogger('jollacn_bot_py.main')

    sys_args = parse()
    config_file = sys_args['--config']
    if not os.path.isabs(config_file):
        config_file = os.path.normpath(os.path.join(PROJECT_PATH, config_file))

    logger.info('load config from file %s', config_file)
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if sys_args['twitter_fetcher']:
        this_config = config['twitter_fetcher']
        logger.info('running twitter_fetcher: %s', twitter_fetcher)
        return twitter_fetcher(
            rabbitmq=config['rabbitmq'],
            fetcher=this_config['fetcher'],
            **this_config['queue']
        )
    else:
        raise RuntimeError(
            'failed to find any runable command: {}'.format(sys_args))


if __name__ == '__main__':
    main()
