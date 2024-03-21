import pandas as pd
from kafka import KafkaProducer
import time
import json

class Producer():
    def __init__(
        self,
        bootstrap_host: str,
        bootstrap_port: str, 
        data_path: str,
        send_topic: str,
        sleep: bool
    ) -> None:
        self.bootstrap_host = bootstrap_host
        self.bootstrap_port = bootstrap_port
        self.data = pd.read_csv(data_path, index_col=0)
        self.send_topic = send_topic
        self.sleep = sleep
    
    def connect(self) -> None:
        self.kafka_producer1 = KafkaProducer(
            bootstrap_servers=[f"{self.bootstrap_host}:{self.bootstrap_port}"],
            value_serializer=lambda x: 
            json.dumps(x).encode('utf-8')
        )
        self.kafka_producer2 = KafkaProducer(
            bootstrap_servers=[f"{self.bootstrap_host}:{self.bootstrap_port}"],
            value_serializer=lambda x: 
            json.dumps(x).encode('utf-8')
        )

    def send(self) -> None:
        length = len(self.data)
        half = int(len(self.data) / 2)
        df1 = self.data.iloc[:half, :]
        df2 = self.data.iloc[half:length, :]
        # change to df
        for n in range(10):
            data1 = n*n
            data2 = 2*n
            print(data1, data2)
            self.kafka_producer1.send("raw_data_topc", value=data1)
            time.sleep(5)
            self.kafka_producer2.send("raw_data_topc", value=data2)

