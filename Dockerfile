FROM python:3.8.6-buster

COPY api /api
COPY resto_project /resto_project
COPY joblibs/model_d2_CA.joblib /joblibs/model_d2_CA.joblib
COPY joblibs/model_d16_CA.joblib /joblibs/model_d16_CA.joblib
COPY joblibs/model_d2_CO.joblib /joblibs/model_d2_CO.joblib
COPY joblibs/model_d16_CO.joblib /joblibs/model_d16_CO.joblib
COPY raw_data/forecasted_services_d2_CA.csv /raw_data/forecasted_services_d2_CA.csv
COPY raw_data/forecasted_services_d16_CA.csv /raw_data/forecasted_services_d16_CA.csv
COPY raw_data/forecasted_services_d2_CO.csv /raw_data/forecasted_services_d2_CO.csv
COPY raw_data/forecasted_services_d16_CO.csv /raw_data/forecasted_services_d16_CO.csv
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
