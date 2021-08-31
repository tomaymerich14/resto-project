from datetime import datetime
import pandas as pd
import joblib
#from Resto_Project_D2.predict import download_model_D2
#from Resto_Project_D2.predict import download_model_D16
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict_CA/?resto_name=D2&date=2012-10-06

###INSERT REQUEST###

###GET RAW DATA###
request_data_d2 = #pd.read_csv('../raw_data/preproc_data_d2.csv')
request_data_d16 = #pd.read_csv('../raw_data/preproc_data_d16.csv')

####TRANSFORM RAW DATA###



###GET PREDICT



@app.get("/")
def index():
    return {"Welcome": "Resto Project"}


@app.get("/predict_CA/")
def create_fare(resto_name,
                date):

    # date = "2013-07-06"
    # service = "midi"

    X = pd.DataFrame(
        dict(resto_name=[resto_name],
             date=[date],
             service=[service]))

    # ⚠️ TODO: get model from GCP

    #pipeline = get_model_from_gcp()
    #pipeline = download_model()
    pipeline_d2 = joblib.load('model_d2.joblib')
    pipeline_d16 = joblib.load('model_d16.joblib')

    # make prediction
    results_d2 = pipeline_d2.predict(X)
    results_d16 = pipeline_d16.predict(X)

    # convert response from numpy to python type
    pred_d2 = float(results_d2[0])
    pred_d16 = float(results_d16[0])

    return dict(prediction=pred_d2), dict(prediction=pred_d16)
