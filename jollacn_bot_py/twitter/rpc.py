#!/usr/bin/env python3
import json
import logging
import pika
from jollacn_bot_py.util import tracemore
from jollacn_bot_py.twitter.fetch import fetch, EXCEPTIONS


class OnRequest(object):

    def __init__(self, fetcher={}):
        self.fetcher = fetcher

    def on_request(self, ch, method, props, body):
        logger = logging.getLogger('jollacn_bot_py.twitter.rpc.on_request')
        logger.info('get request %s', body)
        assert props.reply_to is not None
        args = json.loads(body.decode('utf-8'))
        # urls = args['urls']
        fetcher_args = self.fetcher
        results = []
        for each in args:
            url = each['url']
            try:
                result = fetch(url, **fetcher_args)
            except EXCEPTIONS as e:
                logger.warning('failed to get %s: %s', url, e)
            except BaseException as e:
                logger.error(tracemore.get_exc_plus())
                raise
            else:
                results.append(result)

        # print(results)

        logger.debug('deliverying response')
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=json.dumps(results))
        logger.debug('deliverying ack')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.debug('done')


def rpc(rabbitmq, queue, durable=True, prefetch_count=1, fetcher={}):
    logger = logging.getLogger('jollacn_bot_py.twitter.rpc.rpc')
    logger.info('connecting to %s', rabbitmq)
    username = rabbitmq.pop('username', None)
    password = rabbitmq.pop('password', None)
    if username is not None and password is not None:
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(credentials=credentials, **rabbitmq))
    else:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(**rabbitmq))

    logger.info('connecting channel')
    channel = connection.channel()

    logger.info('declaring queue %s, durable=%s', queue, durable)
    channel.queue_declare(queue=queue, durable=durable)

    logger.info('setting qos prefetch_count=%s', prefetch_count)
    channel.basic_qos(prefetch_count=prefetch_count)
    logger.info('setting consume handler for %s, fetcher=%s', queue, fetcher)
    channel.basic_consume(OnRequest(fetcher).on_request, queue=queue)

    logger.info('startting consuming handler for %s', queue)
    channel.start_consuming()
