from datetime import datetime
import pandas as pd
import joblib
#from Resto_Project_D2.predict import download_model_D2
#from Resto_Project_D2.predict import download_model_D16
from fastapi import FastAPI, File
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

# http://127.0.0.1:8000/predict/

###GET JOBLIB###
model_path = os.path.relpath(os.path.join(
    os.path.dirname(__file__),
    "..",
    "joblibs"))
pipeline_d2_CA = joblib.load(os.path.join(model_path, 'model_d2_CA.joblib'))
pipeline_d16_CA = joblib.load(os.path.join(model_path, 'model_d16_CA.joblib'))
pipeline_d2_CO = joblib.load(os.path.join(model_path, 'model_d2_CO.joblib'))
pipeline_d16_CO = joblib.load(os.path.join(model_path, 'model_d16_CO.joblib'))

###GET RAW DATA###
data_path = os.path.relpath(
    os.path.join(os.path.dirname(__file__), "..", "raw_data"))

request_data_d2_CA = pd.read_csv(os.path.join(data_path, 'forecasted_services_d2_CA.csv'))
request_data_d16_CA = pd.read_csv(os.path.join(data_path, 'forecasted_services_d16_CA.csv'))

request_data_d2_CO = pd.read_csv(os.path.join(data_path, 'forecasted_services_d2_CO.csv'))
request_data_d16_CO = pd.read_csv(os.path.join(data_path, 'forecasted_services_d16_CO.csv'))
####TRANSFORM RAW DATA###
# -> already done mannualy

###GET PREDICT RESULTS###
@app.get("/")
def index():
    return {"Welcome to": "Resto Project"}


@app.post("/uploadfile")
async def create_upload_file(resto_name,file_type,predict,file: bytes = File(...)):

    # resto_name = 'D2' 'D16'
    # file_type = 'csv' 'joblib'
    # predict = 'CA' 'CO' , 'None'

    if resto_name == 'D2':
        if file_type == 'csv':
            if predict == 'CA':
                file_path = "forecasted_services_d2_CA.csv"
            if predict == 'CO':
                file_path = "forecasted_services_d2_CO.csv"
        if file_type == 'joblib':
            if predict == 'CA':
                file_path = "model_d2_CA.joblib"
            if predict == 'CO':
                file_path = "model_d2_CO.joblib"
    if resto_name == 'D16':
        if file_type == 'csv':
            if predict == 'CA':
                file_path = "forecasted_services_d16_CA.csv"
            if predict == 'CO':
                file_path = "forecasted_services_d16_CO.csv"
        if file_type == 'joblib':
            if predict == 'CA':
                file_path = "model_d16_CA.joblib"
            if predict == 'CO':
                file_path = "model_d16_CO.joblib"

    # write file to disk
    with open(file_path, "wb") as f:
        f.write(file)

    # model -> pred
    return dict(pred=True)


@app.get("/predict")
def create_fare():

    # make prediction
    #D2
    results_d2_CA = pipeline_d2_CA.predict(request_data_d2_CA)
    results_d2_CO = pipeline_d2_CO.predict(request_data_d2_CO)
    #D16
    results_d16_CA = pipeline_d16_CA.predict(request_data_d16_CA)
    results_d16_CO = pipeline_d16_CO.predict(request_data_d16_CO)

    # convert response from numpy to python type
    #D2
    pred_d2_CA = results_d2_CA.tolist()
    pred_d2_CO = results_d2_CO.tolist()
    #D16
    pred_d16_CA = results_d16_CA.tolist()
    pred_d16_CO = results_d16_CO.tolist()

    return dict(prediction_D2_CA=pred_d2_CA,
                prediction_D16_CA=pred_d16_CA,
                prediction_D2_CO=pred_d2_CO,
                prediction_D16_CO=pred_d16_CO)
