# Review

We fit the classical machine learning algorithm to predict magnitude of different kind of earthquake, using the [dataset](https://www.kaggle.com/datasets/alessandrolobello/the-ultimate-earthquake-dataset-from-1990-2023/data) both for train and test. We use one million of dataset object for train (80%) and test(20%). The remaining part of the dataset will be used as data from real world, which we will be handle in real-time by [kafka](https://kafka.apache.org/). Result will be reported through streamlit.

# Setup 

1. Set up `PYTHONPATH`:
```bash
export PYTHONPATH=${PYTHONPATH}:${PWD}
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

# Running 
1. Run `zookeeper` and `kafka` images:
```bash 
docker-compose --file ./configs/docker_compose.yaml up 
```

2. For now open terminal and run scripts independently