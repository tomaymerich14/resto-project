from model import get_model_names
from model import get_params_values

max_depth = 4
n_estimators = 40
learning_rate = 0.1

def get_params(model_name):
    if model_name == 'RIDGE':
        mlflow_params_name_1 = get_model_names()[0]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators, learning_rate)

    if model_name == 'DUMMY':
        mlflow_params_name_1 = get_model_names()[1]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)

    if model_name == 'GBR':
        mlflow_params_name_1 = get_model_names()[2]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)

    if model_name == 'XGB':
        mlflow_params_name_1 = get_model_names()[3]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)

    if model_name == 'LGBM':
        mlflow_params_name_1 = get_model_names()[4]
        mlflow_params_value_1 = get_params_values(max_depth, n_estimators,
                                                  learning_rate)

    return mlflow_params_name_1, mlflow_params_value_1
