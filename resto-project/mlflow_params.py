from model import get_model_names
from model import get_params_values

max_depth = 4
n_estimators = 40
learning_rate = 0.1

def get_params(model_name):
    if model_name == 'RIDGE':
        mlflow_params_name_1 = get_model_names()[0]
        mlflow_params_value_1 = get_params_values()[1]

    if model_name == 'DUMMY':
        mlflow_params_name_1 = get_model_names()[0]
        mlflow_params_value_1 = get_params_values()[1]

    if model_name == 'GBR':
        mlflow_params_name_1 = get_model_names()[0]
        mlflow_params_value_1 = get_params_values()[1]

    if model_name == 'XGB':
        mlflow_params_name_1 = get_model_names()[0]
        mlflow_params_value_1 = get_params_values()[1]

    if model_name == 'LGBM':
        mlflow_params_name_1 = get_model_names()[0]
        mlflow_params_value_1 = get_params_values()[1]

<<<<<<< HEAD
=======
    if model_name == 'Dummy':
        mlflow_params_name_1 = 'strategy'
        mlflow_params_value_1 = 'mean'
    if model_name == 'GradientBoostingRegressor':
        mlflow_params_name_1 = 'all_params'
        mlflow_params_value_1 = 'n_estimators=200, verbose=0, max_depth=5, learning_rate=0.05'
    if model_name == 'XGBRegressor':
        mlflow_params_name_1 = 'all_params'
        mlflow_params_value_1 = 'ax_depth=10, n_estimators=300, learning_rate=0.05'
    if model_name == 'lightgbm':
        mlflow_params_name_1 = 'all_params'
        mlflow_params_value_1 = 'all'
>>>>>>> 81c5451afcb9ce4792bf6f6a8eca6a15da9871fb
    return mlflow_params_name_1, mlflow_params_value_1
