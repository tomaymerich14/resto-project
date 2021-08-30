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
    #if model_name == 'tabnet':
       #mlflow_params_name_1 = 'all_params'
       #mlflow_params_value_1 = 'all'
>>>>>>> 00ba87c333c001bd2c9114d85492a6b1453e1a2f
    return mlflow_params_name_1, mlflow_params_value_1
