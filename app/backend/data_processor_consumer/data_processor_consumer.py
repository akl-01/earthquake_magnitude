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

class DataProcessorProducer():
    def __init__(
        self,
        bootstrap_host: str,
        bootstrap_port: str, 
        send_topic: str,
        sleep: bool
    ) -> None:
        self.conf = {
            'bootstrap.servers': f"{bootstrap_host}:{bootstrap_port}"
        }
        self.bootstrap_host = bootstrap_host
        self.bootstrap_port = bootstrap_port
        self.send_topic = send_topic
        self.sleep = sleep
    
    def connect(self) -> None:
        logger.info(f"Connection to {self.bootstrap_host}:{self.bootstrap_port}")
        self.producer = Producer(self.conf)
        logger.info("Connection is established")

    def send(self, data: Any) -> None:
        self.producer.produce(self.send_topic, key='1', value=json.dumps(data))
        self.producer.flush()
        logger.info(f"Produced: {data}")
        if self.sleep:
            time.sleep(10)

class DataProcessorConsumer():
    def __init__(
        self,
        bootstrap_host: str,
        bootstrap_port: str, 
        read_topic: str,
    ) -> None:
        self.conf = {
            'bootstrap.servers': f"{bootstrap_host}:{bootstrap_port}", 
            'group.id': 'dp_consumer',
        }
        self.bootstrap_host = bootstrap_host
        self.bootstrap_port = bootstrap_port
        self.read_topic = read_topic
    
    @property
    def producer(self) -> Any:
        _producer = DataProcessorProducer(
            bootstrap_host="localhost",
            bootstrap_port="9096",
            send_topic="processed_data_topic",
            sleep=True
        )
        _producer.connect()

        return _producer


    def connect(self) -> None:
        logger.info(f"Connection to {self.bootstrap_host}:{self.bootstrap_port}")
        self.consumer = Consumer(self.conf)
        self.consumer.subscribe([self.read_topic])
        logger.info("Connection is established")
    
    def read(self) -> None:
        logger.info("Get producer")
        producer = self.producer
        logger.info(f"Read data from {self.read_topic}")
        # preprocess and send
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
    consumer = DataProcessorConsumer(
        bootstrap_host="localhost",
        bootstrap_port="9095",
        read_topic="raw_data_topic"
    )

    consumer.connect()
    consumer.read()