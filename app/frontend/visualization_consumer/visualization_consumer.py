from confluent_kafka import Consumer
import logging as log
import json
from typing import Any
import plotly.express as px
import pandas as pd

import streamlit as st 

logger = log.getLogger(__name__)
logger.setLevel(log.INFO)
console = log.StreamHandler()
console_formater = log.Formatter("[ %(levelname)s ] %(message)s")
console.setFormatter(console_formater)
logger.addHandler(console)

st.set_page_config(
    page_title="Real-Time Data Dashboard",
    layout="wide",
)

if "magnitude" not in st.session_state:
    st.session_state["magnitude"] = []
if "mae" not in st.session_state:
    st.session_state["mae"] = []
if "mse" not in st.session_state:
    st.session_state["mse"] = []

st.title("Real-time metrics")
st.subheader("Magnitude")
mag_chart_holder = st.empty()
st.subheader("MAE")
mae_chart_holder = st.empty()
st.subheader("MSE")
mse_chart_holder = st.empty()

class VisualizationConsumer():
    def __init__(
        self,
        bootstrap_host: str,
        bootstrap_port: str, 
        read_topic: str,
    ) -> None:
        self.conf = {
            'bootstrap.servers': f"{bootstrap_host}:{bootstrap_port}", 
            'group.id': 'vs_consumer',
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
            data = json.loads(msg.value().decode('utf-8'))

            st.session_state["magnitude"].append(data['predict'])
            st.session_state["mae"].append(data["mae"])
            st.session_state["mse"].append(data["mse"])

            mag_chart_holder.line_chart(st.session_state["magnitude"])
            mae_chart_holder.line_chart(st.session_state["mae"])
            mse_chart_holder.line_chart(st.session_state["mse"])
            

if __name__ == "__main__":
    consumer = VisualizationConsumer(
        bootstrap_host="localhost",
        bootstrap_port="9095",
        read_topic="ml_results_topic"
    )

    consumer.connect()
    consumer.read()