import asyncio
import json
import logging
import os
import time
from typing import List

import azure.functions as func

from .chat import  get_sql_code, FullProcessing
from .prompt import get_prompt_sources, PromptIndex
from ..receive.producer import Producer
from ..send_message.cache import Redis

# declare static variables
chat_model = '<gpt-35-turbo model name>'
embeddings_model = '<ada-embeddings model name>'

# instaciate reference table
prompts_sources = get_prompt_sources('chat_call/')
prompts_index = PromptIndex(embeddings_model, prompts_sources)

# declare event hub variables
SEND_MESSAGE = 'send-message'
EXECUTE_CODE = 'execute'
CONN_STRING = os.environ.get('CONN_STRING')

# instanciate event hub Producer to send messages
send = Producer(CONN_STRING, SEND_MESSAGE)
execute = Producer(CONN_STRING, EXECUTE_CODE)

# Instanciate Redis cache
redis = Redis()


def main(events: List[func.EventHubEvent]):
    logging.info('Python EventHub triggered')
    event = json.loads(events.get_body().decode('UTF-8'))
    logging.info(f'Received event is: {event}')
    message = event['body']
    sender = event['from']

    if 'loop' in event.keys():
        loop = event['loop']
    else:
        loop = False
    
    chat = FullProcessing(question = message,
                          sender = sender,
                          chat_model = chat_model,
                          reference_table = prompts_index,
                          loop = loop)
    try:
        response = chat.send_message()
    except Exception as e:
        logging.info('Error calling chatGPT API, waiting 3 seconds')
        logging.info(f'Error: {e}')
        time.sleep(3)
        response = chat.send_message()

    logging.info(f'chat response is : {response}')
    
    event['response.text'] = response
    code = get_sql_code(response)
    event['prompt.name'] = chat.reference_table.prompt_name
    logging.info(f'prompt name is : {event["prompt.name"]}')
    event['body'] = chat.question
    logging.info(f'updated, after cache, body is : {event["body"]}')
    if response != code:
        event['response.code'] = code
        logging.info('sending to EXECUTE queue')
        asyncio.run(execute.send_events([event]))
    else:
        logging.info('sending to SEND queue')
        redis.set_cache(event)
        asyncio.run(send.send_events([event]))