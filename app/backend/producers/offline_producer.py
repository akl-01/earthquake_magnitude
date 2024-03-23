import pandas as pd
import numpy as np
from confluent_kafka import Producer
import time
import json
import logging as log

from utils import delivery_report

logger = log.getLogger(__name__)
logger.setLevel(log.INFO)
console = log.StreamHandler()
console_formater = log.Formatter("[ %(levelname)s ] %(message)s")
console.setFormatter(console_formater)
logger.addHandler(console)

class OfflineProducer():
    def __init__(
        self,
        bootstrap_host: str,
        bootstrap_port: str, 
        data_path: str,
        send_topic: str,
        sleep: bool
    ) -> None:
        self.conf = {
            'bootstrap.servers': f"{bootstrap_host}:{bootstrap_port}"
        }
        self.bootstrap_host = bootstrap_host
        self.bootstrap_port = bootstrap_port
        self.data = pd.read_csv(data_path, index_col=0)
        self.send_topic = send_topic
        self.sleep = sleep
    
    def connect(self) -> None:
        logger.info(f"Connection to {self.bootstrap_host}:{self.bootstrap_port}")
        self.producer = Producer(self.conf)
        logger.info("Connection is established")

    def send(self) -> None:
        low = 0
        high = len(self.data)
        logger.info(f"Sending data to {self.send_topic}")
        while True:
            df_entry = self.data.iloc[np.random.randint(low=low, high=high), :]
            temp = pd.Series({"real_time": 0})
            data = pd.concat([df_entry, temp])
            data = data.to_json()
            self.producer.produce(self.send_topic, value=data, callback=delivery_report)
            self.producer.flush()
            if self.sleep:
                time.sleep(100)

if __name__ == "__main__":
    csv_path = "./data/earthquake_1995-2023.csv"
    producer = OfflineProducer(
        bootstrap_host="localhost",
        bootstrap_port="9095",
        data_path=csv_path,
        send_topic="raw_data_topic",
        sleep=True
    )

    producer.connect()
    producer.send()