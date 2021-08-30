from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import StackingRegressor
from trainer import set_params


def get_params_values():
    return f'max_depth = {set_params()[0]}', f'n_estimators = {set_params()[1]}', f'learning_rate = {set_params()[2]}'


def get_params_names():
    return 'max_depth', 'n_estimators', 'learning_rate'


def get_model_names():
    return 'RIDGE', 'DUMMY', 'GBR', 'XGB', 'LGBM', 'CATB'

class Trainer():
def model_selection(model_test, *args):
    if model_test == 'RIDGE':
        model_test = Ridge()

    if model_test == 'DUMMY':
        model_test = DummyRegressor(strategy='mean')

    if model_test == 'GBR':
        model_test = GradientBoostingRegressor(max_depth, n_estimators,learning_rate)

    if model_test == 'XGB':
        model_test = XGBRegressor(max_depth,n_estimators,learning_rate)

    if model_test == 'LGBM':
        model_test = LGBMRegressor(max_depth, n_estimators, learning_rate)

    if model_test == 'CATB':
        model_test = CatBoostRegressor(max_depth, n_estimators, learning_rate)

    return model_test
