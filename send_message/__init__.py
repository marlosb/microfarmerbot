import json
import logging
from typing import List

import azure.functions as func

from .send import send_message

def main(events: List[func.EventHubEvent]):
    logging.info('Python EventHub triggered')
    event = json.loads(events.get_body().decode('UTF-8'))
    logging.info(f'Received event is: {event}')

    send_message(event)