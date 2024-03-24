import pandas as pd
import numpy as np
from confluent_kafka import Producer
from confluent_kafka import Consumer
import time
import json
import logging as log
from typing import Any
from utils import delivery_report

from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

logger = log.getLogger(__name__)
logger.setLevel(log.INFO)
console = log.StreamHandler()
console_formater = log.Formatter("[ %(levelname)s ] %(message)s")
console.setFormatter(console_formater)
logger.addHandler(console)

class MLProducer():
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
        self.producer.produce(self.send_topic, key='1', value=json.dumps(data), callback=delivery_report)
        self.producer.flush()
        logger.info(f"Produced: {data}")
        if self.sleep:
            time.sleep(10)

class MLConsumer():
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
    def producer(self) -> Any:
        _producer = MLProducer(
            bootstrap_host="localhost",
            bootstrap_port="9095",
            send_topic="ml_results_topic",
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
        _producer = self.producer
        logger.info(f"Read data from {self.read_topic}")
        model = CatBoostRegressor(
            iterations=4200,
            learning_rate=1,
            depth=3,
            loss_function="RMSE"
        )
        model.load_model("./weights/model.pkl")
        # run model and send results
        while True:
            msg = self.consumer.poll(10)
            if msg is None:
                logger.info("Message is None")
                continue
            if msg.error():
                logger.info("Consumer error: {}".format(msg.error()))
                continue
        
            logger.info('Received message: {}'.format(msg.value().decode('utf-8')))

            df = pd.read_json(msg.value().decode('utf-8'), orient="index")
            df = df.transpose()
            X, y = df.drop(["magnitude"], axis=1), df["magnitude"]
            predict = model.predict(X)
            mae = mean_absolute_error(y, predict)
            mse = mean_squared_error(y, predict)
            results = {
                "predict": predict.tolist(),
                "mae": mae,
                "mse": mse
            }
            _producer.send(results)



if __name__ == "__main__":
    consumer = MLConsumer(
        bootstrap_host="localhost",
        bootstrap_port="9096",
        read_topic="processed_data_topic"
    )

    consumer.connect()
    consumer.read()