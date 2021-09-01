import requests

# fill the parameters for the prediction
params = dict(date='2012-10-06',
              service='midi')

# URL
resto_api_url = "http://127.0.0.1:8000/predict"

# retrieve the response
response = requests.get(resto_api_url, params=params)

if response.status_code == 200:
    print("API call success")
else:
    print("API call error")

response.status_code, response.json().get("prediction",
                                          "no prediction"), response.json()
