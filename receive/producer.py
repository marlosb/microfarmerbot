import json
import logging

from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

class Producer:
    def __init__(self, 
                connection_string: str, 
                eventhub_name: str) -> None:
        self.producer = EventHubProducerClient.from_connection_string(
                        conn_str=connection_string,
                        eventhub_name=eventhub_name)

    async def prepare_events(self, events_list: list[dict]):
        logging.info('creating empty event data batch')
        async with self.producer:
            event_data_batch = await self.producer.create_batch()
            logging.info(f'adding {len(events_list)} events to batch')
            for event in events_list:
                event_str = json.dumps(event)
                logging.info(f'event is {event_str}')
                event_data_batch.add(EventData(event_str))
            logging.info('batch of events sucessfully created')
        return event_data_batch

    async def send_events(self, events_list: list[dict]) -> None:
        event_data_batch = await self.prepare_events(events_list = events_list)
        logging.info('sending batch of events')
        async with self.producer:
            await self.producer.send_batch(event_data_batch)
        logging.info('batch of events sucessfully sent')

    def close(self) -> None:
        self.producer.close()