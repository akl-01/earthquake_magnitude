import pandas as pd
import numpy as np
from confluent_kafka import Producer
import time
import logging as log
from typing import Any
import json

import urllib.request
import datetime
from libcomcat.search import search 

from utils import delivery_report

logger = log.getLogger(__name__)
logger.setLevel(log.INFO)
console = log.StreamHandler()
console_formater = log.Formatter("[ %(levelname)s ] %(message)s")
console.setFormatter(console_formater)
logger.addHandler(console)

class RealTimeProducer():
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

    def real_time(self) -> Any:
        logger.info(f"Getting real time data")
        #start_time = datetime.datetime.now()
        #time.sleep(10)
        start_date = datetime.datetime.now().date()
        start_time = datetime.time.min
        start_time = datetime.datetime.combine(start_date, start_time)
        end_time = datetime.datetime.now()
        events = search(starttime=start_time, endtime=end_time)
        logger.info(f"Returned {len(events)} events")

        return events
    
    def connect(self) -> None:
        logger.info(f"Connection to {self.bootstrap_host}:{self.bootstrap_port}")
        self.producer = Producer(self.conf)
        logger.info("Connection is established")

    def send(self) -> None:
        logger.info(f"Sending data to {self.send_topic}")
        while True:
            events = self.real_time()

            for event in events:
                with urllib.request.urlopen(event["detail"]) as url:
                    data = json.load(url)["properties"]
                data["real_time"] = 1
                data = pd.DataFrame(data)
                data = data.loc["origin"].to_frame().transpose().reset_index()
                data = data.drop(["index"], axis=1)
                data = data.to_json()

                self.producer.produce(self.send_topic, value=data, callback=delivery_report)
                self.producer.flush()
                if self.sleep:
                    time.sleep(5)

if __name__ == "__main__":
    producer = RealTimeProducer(
        bootstrap_host="localhost",
        bootstrap_port="9095",
        send_topic="raw_data_topic",
        sleep=True
    )

    producer.connect()
    producer.send()