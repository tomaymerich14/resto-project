import pandas as pd
import numpy as np


def get_params(model_name):
    if model_name == 'Ridge':
        mlflow_params_name_1 = ''
        mlflow_params_value_1 = ''
    if model_name == 'Dummy':
        mlflow_params_name_1 = 'strategy'
        mlflow_params_value_1 = 'mean'
    if model_name == 'GradientBoostingRegressor':
        mlflow_params_name_1 = 'all_params'
        mlflow_params_value_1 = 'n_estimators=200, verbose=0, max_depth=5, learning_rate=0.05'
    if model_name == 'XGBRegressor':
        mlflow_params_name_1 = 'all_params'
        mlflow_params_value_1 = 'ax_depth=10, n_estimators=300, learning_rate=0.05'
    return mlflow_params_name_1, mlflow_params_value_1
