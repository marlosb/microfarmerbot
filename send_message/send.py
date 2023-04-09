import logging
import os

import requests

def send_message(event: dict)-> None:
    '''
    Function to select channel and call appropriated send function.

    parameters:
    event (dict): event dict with all information from request, channel and response
    '''
    if event['channel'] == 'whatsapp':
        logging.info('sending message to whatsapp')
        whatsapp_send(event['response.text'], event['from'])
    elif event[ 'channel'] == 'telegram':
        logging.info('sending message to telegram')
        telegram_send(event['response.text'], event['from'])
    else:
        logging.info(f'Do not know which channel to send, event channle is: {event["channel"]}')

def telegram_send(message: str, destination_numder: int) -> None:
    ''' 
    Function to send message to Telegram
    Using Telegram Bot API and python requests library

    parameters:
    message (str): message to send
    destination_number (int): telegram ID to send message
    '''

    token = os.environ['TELEGRAM_TOKEN']
    send_url = f'https://api.telegram.org/bot{token}/sendMessage'   

    body = {
        "text":f'{message}',
        "chat_id":destination_numder
        }
    logging.info(f'body is {body}')

    response = requests.get(send_url, params = body)
    logging.info('response message sent')
    logging.info(f'reponse status code is {response.status_code}')
    logging.info(f'reponse text is {response.text}')

def whatsapp_send(message: str, destination_number: str) -> None:
    '''
    Function to send message to WhatsApp
    Using Whatsapp Cloud API and python requests library

    parameters:
    message (str): message to send
    destination_number (str): whatsapp ID (phone number) to send message
    '''
    # URL to send message
    url = 'https://graph.facebook.com/v16.0/122535937426425/messages'
    # Token
    token = os.environ['WHATSAPP_TOKEN']

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'}
    logging.info(f'headers are {headers}')

    body = {
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': f'{destination_number}',
        'type': 'text',
        'text': {'body': f'{message}'}}
    logging.info(f'body is {body}')

    #response = requests.post(url, headers=headers, json=body)
    logging.info('response message sent')
    #logging.info(f'reponse status code is {response.status_code}')
    #logging.info(f'reponse text is {response.text}')