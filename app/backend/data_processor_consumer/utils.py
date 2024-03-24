import pandas as pd
from typing import Any

IMPORTANT_FEATURES = [
    'sig', 'cdi', 'longitude', 'latitude', 
    'depth', 'gap','dmin',
    'nst', 'mmi', 'net']
TARGET = ["magnitude"]

INT_FEATURES = [
    "sig", "cdi", "official", "nst", "mmi"
]
FLOAT_FEATURES = [
    "longitude", "latitude", "depth", "gap", "dmin", "magnitude"
]

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={"mag":"magnitude"})   
    return df

def complete(df: pd.DataFrame) -> pd.DataFrame:
    values = {}
    temp = df["products"][0][0]["properties"]
    values["longitude"] = [temp["longitude"]]
    values["latitude"] = [temp["latitude"]]
    values["depth"] = [temp["depth"]]

    temp_df = pd.DataFrame(values)

    return df.join(temp_df)

def net2office(df: pd.DataFrame) -> pd.DataFrame:
    if df["net"].values == "official":
        df["net"][0] = 1
    else: 
        df["net"][0] = 0
    
    df = df.rename(columns={"net": "official"})
    
    return df

def fill_none(df: pd.DataFrame) -> pd.DataFrame:
    values = {
        'sig': 0,
        'cdi': 0, 
        'longitude': 0,
        'latitude': 0, 
        'depth': 0, 
        'gap': 180,
        'dmin': 1000,
        'nst': 0, 
        'mmi': 0, 
        'net': "ak"
    } 
    df = df.fillna(value=values)
    return df

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    if df["real_time"].values == 1:
        df = rename_columns(df)
        df = complete(df)
    df = df[IMPORTANT_FEATURES + TARGET]
    df = fill_none(df)
    df = net2office(df)
    df[INT_FEATURES] = df[INT_FEATURES].astype(int)
    df[FLOAT_FEATURES] = df[FLOAT_FEATURES].astype(float)

    return df

