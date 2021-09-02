FROM python:3.8.6-buster

COPY api /api
COPY resto_project /resto_project
COPY joblibs /joblibs
COPY raw_data/forecasted_services_d2_CA.csv /raw_data/forecasted_services_d2_CA.csv
COPY raw_data/forecasted_services_d16_CA.csv /raw_data/forecasted_services_d16_CA.csv
COPY raw_data/forecasted_services_d2_CO.csv /raw_data/forecasted_services_d2_CO.csv
COPY raw_data/forecasted_services_d16_CO.csv /raw_data/forecasted_services_d16_CO.csv
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
