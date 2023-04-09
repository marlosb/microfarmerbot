import asyncio
import json
import logging
import os

import azure.functions as func

from .producer import Producer

FILTER_OBJECT = 'whatsapp_business_account'
ALLOWEDS_NUMBERS = ['<phone number 1>', '<phone number 2']
TOPIC_NAME = 'chat-ready'
CONN_STRING = os.environ.get('CONN_STRING')

producer = Producer(CONN_STRING, TOPIC_NAME)

def traverse(data: dict, flat_dict: dict) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                traverse(value, flat_dict)
            else:
                flat_dict[key] = value
    elif isinstance(data, list):
        for item in data:
            traverse(item, flat_dict)

def handle_messages(message: dict) -> None:
    if message['object'] == FILTER_OBJECT:
        message_flat = {}
        traverse(message['entry'], message_flat)
        message_flat['channel'] = 'whatsapp'
        logging.info(f'Flatten message is {message_flat}')
    return message_flat

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(f'request method is: {req.method}')

    verify_token = 'AAAA4444GGGG888'
    params = req.params

    if ('hub.verify_token' in params.keys()) and (params['hub.verify_token'] == verify_token):
        challenge = params['hub.challenge']
        logging.info(f'Passed verification, challenge is {challenge}')
    else:
        challenge = 'None'

    if req.method == 'POST':
        try:
            message = handle_messages(json.loads(req.get_body()))
            if 'body' in message.keys() and message['from'] in ALLOWEDS_NUMBERS:
                asyncio.run(producer.send_events([message]))
        except:
            logging.info('No body message, ignoring request!')

    return func.HttpResponse(challenge, status_code=200)