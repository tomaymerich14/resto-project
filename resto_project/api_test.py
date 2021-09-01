from datetime import datetime
import pandas as pd
import joblib
#from Resto_Project_D2.predict import download_model_D2
#from Resto_Project_D2.predict import download_model_D16
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# http://127.0.0.1:8000/predict/

###INSERT REQUEST###
pipeline_d2 = joblib.load('../joblibs/model_d2.joblib')
pipeline_d16 = joblib.load('../joblibs/model_d16.joblib')
###GET RAW DATA###
request_data_d2 = pd.read_csv('../raw_data/forecasted_services_d2.csv')
request_data_d16 = pd.read_csv('../raw_data/forecasted_services_d16.csv')

#request_data_d2 = request_data_d2.drop(columns=["CA_TTC"])
#request_data_d16 = request_data_d16.drop(columns=["CA_TTC"])

####TRANSFORM RAW DATA###
# -> already done mannualy

###GET PREDICT

@app.get("/")
def index():
    return {"Welcome to": "Resto Project"}


@app.get("/predict/")
def create_fare():
    #def create_fare(date, service, match_edf, roland_garros, fashion_week,
    #       match_happening, match_happening_cl, temp, feels_like,
    #       temp_min, temp_max, wind_speed, clouds_all, vacances_paris,
    #       clear, clouds, drizzle, drizzle_and_rain, fog, mist, rain,
    #       thunderstorm):

    # date = "2013-07-06"
    # service = "midi"
    #resto_name = 'D2'



    # ⚠️ TODO: get model from GCP

    #pipeline = get_model_from_gcp()
    #pipeline = download_model()


    # make prediction
    results_d2 = pipeline_d2.predict(request_data_d2)
    results_d16 = pipeline_d16.predict(request_data_d16)

    # convert response from numpy to python type
    pred_d2 = results_d2.tolist()
    pred_d16 = results_d16.tolist()

    return dict(prediction_D2_CA=pred_d2, prediction_D16_CA=pred_d16)
