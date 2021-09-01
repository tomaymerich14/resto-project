FROM python:3.8.6-buster

COPY api /api
COPY resto_project /resto_project
COPY joblibs/model_d2.joblib /joblibs/model_d2.joblib
COPY joblibs/model_d16.joblib /joblibs/model_d16.joblib
COPY raw_data/preproc_data_d2.csv /raw_data/preproc_data_d2.csv
COPY raw_data/preproc_data_d16.csv /raw_data/preproc_data_d16.csv
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
