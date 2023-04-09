import asyncio
import json
import logging
import os
from typing import List

import azure.functions as func

from .sqlrun import execute_sql_code
from ..receive.producer import Producer
from ..send_message.cache import Redis

# declare event hub variables
CHAT_READY = 'chat-ready'
SEND_MESSAGE = 'send-message'
CONN_STRING = os.environ.get('CONN_STRING')

# instanciate event hub Producer to send messages
send = Producer(CONN_STRING, SEND_MESSAGE)
chat = Producer(CONN_STRING, CHAT_READY)

# forbidden keywords
forbidden = ['drop', 'delete', 'truncate', 'alter', 'create']

# Instanciate Redis cache
redis = Redis()

def main(events: List[func.EventHubEvent]):
    logging.info('Python EventHub triggered')
    event = json.loads(events.get_body().decode('UTF-8'))

    logging.info(f'Event is: {event}')
    if 'loop' in event.keys() and event['loop'] == True :
        logging.info('System in looping, breaking it.')
        asyncio.run(send.send_events([event]))
        event['loop'] = False
        return
        
    code = event["response.code"]
    logging.info(f'code to be executed is: {code}')

    safe_flag = True
    for word in forbidden:
        if word in code.lower():
            safe_flag = False
            break

    if not safe_flag:
        event['response.text'] = 'Foi detectada uma keyword não autorizada, pedido recusado. Por favor, reformule'
        logging.info(f'forbidden keyword detected')
        input_flag = True
    else:
        logging.info('Code is safe, executing...')
        input_flag, output = execute_sql_code(code)

    logging.info(f'Response from DB is {output}')
    logging.info(f'Input flag is {input_flag}')
    redis.set_cache(event)
    if input_flag:
        event['loop'] = False
        event['response.text'] = output
        asyncio.run(send.send_events([event]))
        logging.info('Event sent to SEND queue')
    else:
        event['loop'] = True
        event['body'] = 'Executei o código e a resposta foi: ' + output + '\Descreva com texto o resultado, de forma bem sucinta, para um usuário sem conhecimento técnico, sem usar código SQL ou detalhes da tabela'
        asyncio.run(chat.send_events([event]))
        logging.info('Event sent to CHAT queue')