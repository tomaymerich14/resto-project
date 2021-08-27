#SKLEARN
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.dummy import DummyRegressor


def model_selection(model_name):
    if model_name == 'Ridge':
        model_test = Ridge()
    if model_name == 'Dummy':
        model_test = DummyRegressor(strategy='mean')
    return model_test
