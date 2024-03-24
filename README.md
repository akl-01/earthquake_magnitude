# Review

We employ the classical machine learning algorithm to predict magnitude of different kind of earthquake, using the [dataset](https://www.kaggle.com/datasets/warcoder/earthquake-dataset?select=earthquake_data.csv) both for train and test. Next we will get real-time data both from [source](https://earthquake.usgs.gov/fdsnws/event/1/#methods) and csv file, which we will be handle by [kafka](https://kafka.apache.org/). Result will be reported through streamlit.

# Setup 

1. Install requirements:
```bash
pip install -r requirements.txt
```
2. Run the script:
```bash
python3 run.py
```