# Review

We employ the classical machine learning algorithm to predict magnitude of different kind of earthquake, using the [dataset](https://www.kaggle.com/datasets/warcoder/earthquake-dataset?select=earthquake_data.csv) both for train and test. Next we will get real-time data from [source](https://earthquake.usgs.gov/fdsnws/event/1/#methods), which we will be handle by [kafka](https://kafka.apache.org/). Result will be reported through streamlit.

# Setup 

1. Install requirements:
```bash
pip install -r requirements.txt
```

# Running 
1. Run `zookeeper` and `kafka` images:
```bash 
docker-compose --file ./configs/docker_compose.yaml up 
```

2. For now open terminal and run scripts independently