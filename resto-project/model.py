from pandas.core.algorithms import mode
from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from tabnet import TabNetClassifier, TabNetRegressor
from catboost import CatBoostRegressor

model_name = 'XGB'
max_depth = 4
n_estimators = 40
learning_rate = 0.1

def get_params_values(max_depth, n_estimators, learning_rate):
    params = f'max_depth = {max_depth}, n_estimators = {n_estimators}, learning_rate = {learning_rate}'
    return params

def get_params_names():
    return 'max_depth', 'n_estimators', 'learning_rate'

def get_model_names():
    models = ['RIDGE', 'DUMMY', 'GBR', 'XGB', 'LGBM', 'CATB']
    return models

def model_selection(model_name):
    if model_name == 'RIDGE':
        model_test = Ridge()

    if model_name == 'DUMMY':
        model_test = DummyRegressor(strategy='mean')

    if model_name == 'GBR':
        model_test = GradientBoostingRegressor(max_depth=max_depth,
                                               n_estimators=n_estimators,
                                               learning_rate=learning_rate)

    if model_name == 'XGB':
        model_test = XGBRegressor(max_depth=max_depth,
                                  n_estimators=n_estimators,
                                  learning_rate=learning_rate)

    if model_name == 'LGBM':
        model_test = LGBMRegressor(max_depth=max_depth,
                                   n_estimators=n_estimators,
                                   learning_rate=learning_rate)

    if model_name == 'CATB':
        model_test = CatBoostRegressor(max_depth=max_depth,
                                       n_estimators=n_estimators,
                                       learning_rate=learning_rate)

    #if model_name == 'tabnet':
        #model_test = TabNetRegressor()

    return model_test


if __name__ == '__main__':
    get_model_names()
    get_model_names()
    model_selection()
