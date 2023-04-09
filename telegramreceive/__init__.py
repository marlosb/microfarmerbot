import asyncio
import json
import logging
import os

import azure.functions as func

from ..receive import traverse
from ..receive.producer import Producer

ALLOWEDS_NUMBERS = [<chat ID 1>, <chat ID 1>]
TOPIC_NAME = 'chat-ready'
CONN_STRING = os.environ.get('CONN_STRING')

producer = Producer(CONN_STRING, TOPIC_NAME)

def handle_messages(message: dict) -> None:
    message_flat = {}
    traverse(message, message_flat)
    message_flat['body'] = message_flat.pop('text')
    message_flat['from'] = message_flat.pop('id')
    message_flat['channel'] = 'telegram'
    logging.info(f'Flatten message is {message_flat}')
    return message_flat

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(f'request method is: {req.method}')
    logging.info(f'request body before handling is: {req.get_body()}')

    if req.method == 'POST':
        try:
            message = handle_messages(json.loads(req.get_body()))
            if 'body' in message.keys() and message['from'] in ALLOWEDS_NUMBERS:
                asyncio.run(producer.send_events([message]))

        except Exception as e:
            logging.info(f'No body message, ignoring request!\n{e}')

    return func.HttpResponse( "ok",status_code=200)