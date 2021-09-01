from model import get_model_names
from model import get_params_values
from __main__ import max_depth, n_estimators, learning_rate, model_name

model_name = model_name

def get_params(model_name):
    if model_name == 'RIDGE':
        i = 0
        mlflow_params_name_1 = get_model_names()[i]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)
        mlflow_params_name_2 = get_model_names()[i]
        mlflow_params_value_2 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)

    if model_name == 'DUMMY':
        i = 1
        mlflow_params_name_1 = get_model_names()[i]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)
        mlflow_params_name_2 = get_model_names()[i]
        mlflow_params_value_2 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)

    if model_name == 'GBR':
        i = 2
        mlflow_params_name_1 = get_model_names()[i]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)
        mlflow_params_name_2 = get_model_names()[i]
        mlflow_params_value_2 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)

    if model_name == 'XGB':
        i = 3
        mlflow_params_name_1 = get_model_names()[i]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)
        mlflow_params_name_2 = get_model_names()[i]
        mlflow_params_value_2 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)
    if model_name == 'LGBM':
        i = 4
        mlflow_params_name_1 = get_model_names()[i]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)
        mlflow_params_name_2 = get_model_names()[i]
        mlflow_params_value_2 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)

    return mlflow_params_name_1, mlflow_params_value_1, mlflow_params_name_2, mlflow_params_value_2
