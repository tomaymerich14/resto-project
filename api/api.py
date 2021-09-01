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
pipeline_d2 = joblib.load(os.path.join(model_path, 'model_d2.joblib'))
pipeline_d16 = joblib.load(os.path.join(model_path, 'model_d16.joblib'))

###GET RAW DATA###
data_path = os.path.relpath(
    os.path.join(os.path.dirname(__file__), "..", "raw_data"))

request_data_d2 = pd.read_csv(os.path.join(data_path, 'forecasted_services_d2.csv'))
request_data_d16 = pd.read_csv(os.path.join(data_path, 'forecasted_services_d16.csv'))

####TRANSFORM RAW DATA###
# -> already done mannualy

###GET PREDICT RESULTS###
@app.get("/")
def index():
    return {"Welcome to": "Resto Project"}


@app.post("/uploadfile")
async def create_upload_file(resto_name,file: bytes = File(...)):

    # print("\nreceived file:")
    # print(type(file))
    # print(file)

    if resto_name == 'd2':
        file_path = "forecasted_services_d2.csv"
    if resto_name == 'd16':
        file_path = "forecasted_services_d16.csv"


    # write file to disk
    with open(file_path, "wb") as f:
        f.write(file)

    # model -> pred
    return dict(pred=True)


@app.get("/predict")
def create_fare():

    # make prediction
    #D2
    results_d2 = pipeline_d2.predict(request_data_d2)
    #D16
    results_d16 = pipeline_d16.predict(request_data_d16)

    # convert response from numpy to python type
    pred_d2 = results_d2.tolist()
    pred_d16 = results_d16.tolist()

    return dict(prediction_D2_CA=pred_d2, prediction_D16_CA=pred_d16)
