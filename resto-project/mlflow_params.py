import pandas as pd
import numpy as np


def get_params(model_name):
    if model_name == 'Ridge':
        mlflow_params_name_1 = 'Ridge'
        mlflow_params_value_1 = 'no params'

    if model_name == 'Dummy':
        mlflow_params_name_1 = 'strategy'
        mlflow_params_value_1 = 'mean'
    return mlflow_params_name_1, mlflow_params_value_1
