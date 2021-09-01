FROM python:3.8.6-buster

COPY api /api
COPY resto_project /resto_project
COPY model_d2.joblib /model_d2.joblib
COPY model_d16.joblib /model_d16.joblib
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
