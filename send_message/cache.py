import logging
import os

import redis

class Redis():
    def __init__(self, port: int = 6380, ttl_seconds: int = 180):
        self.hostname = os.environ['REDIS_HOSTNAME']
        self.password = os.environ['REDIS_PASSWORD']
        self.ttl_seconds = ttl_seconds # default = 180 seconds = 3 minutes
        self.cache = None
        self.connection = redis.StrictRedis(host = self.hostname, 
                                                    port = port, 
                                                    password = self.password, 
                                                    ssl = True)
    
    def set_cache(self, event):
        message = event['response.text']
        sender = event['from']
        body = event['body']
        logging.info(f'Message sender is: {sender}')
        logging.info(f'Response message is: {message}') 
        logging.info(f'Body is: {body}') 

        to_cache = body + '\nassistant\n' + message
        logging.info(f'Setting cache message: {to_cache}')        
        self.connection.set(sender, to_cache, ex=self.ttl_seconds)
    
    def _check_cache(self, sender):
        cached_response = self.connection.get(sender)
        if cached_response:
            logging.info('Cached response found, retrieving from cache')
            self.cache = cached_response.decode('UTF-8')
            logging.info(f'Cached data is: {self.cache}')
        else:
            logging.info('No cached response found')
            self.cache = None
    
    def read_cache(self, sender):
        self._check_cache(sender)
        return self.cache
    
    def reset_cache(self, event):
        sender = event['from']
        self.connection.set(sender, ' ', ex=1)
        self._check_cache(sender)
        return self.cache