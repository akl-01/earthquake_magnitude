import pandas as pd
import numpy as np
from confluent_kafka import Producer
from confluent_kafka import Consumer
import time
import json
import logging as log
from typing import Any

logger = log.getLogger(__name__)
logger.setLevel(log.INFO)
console = log.StreamHandler()
console_formater = log.Formatter("[ %(levelname)s ] %(message)s")
console.setFormatter(console_formater)
logger.addHandler(console)

class Stremlit():
    pass

class VisualizationConsumer():
    def __init__(
        self,
        bootstrap_host: str,
        bootstrap_port: str, 
        read_topic: str,
    ) -> None:
        self.conf = {
            'bootstrap.servers': f"{bootstrap_host}:{bootstrap_port}", 
            'group.id': 'ml_consumer',
        }
        self.bootstrap_host = bootstrap_host
        self.bootstrap_port = bootstrap_port
        self.read_topic = read_topic
    
    @property
    def stremlit(self) -> Any:
        pass

    def connect(self) -> None:
        logger.info(f"Connection to {self.bootstrap_host}:{self.bootstrap_port}")
        self.consumer = Consumer(self.conf)
        self.consumer.subscribe([self.read_topic])
        logger.info("Connection is established")
    
    def read(self) -> None:
        logger.info("Get producer")
        stremlit = self.stremlit
        logger.info(f"Read data from {self.read_topic}")
        # get the data and send to stremlit
        while True:
            msg = self.consumer.poll(10)
            if msg is None:
                logger.info("Message is None")
                continue
            if msg.error():
                logger.info("Consumer error: {}".format(msg.error()))
                continue
            
            logger.info('Received message: {}'.format(msg.value().decode('utf-8')))


if __name__ == "__main__":
    consumer = VisualizationConsumer(
        bootstrap_host="localhost",
        bootstrap_port="9095",
        read_topic="ml_results_topic"
    )

    consumer.connect()
    consumer.read()