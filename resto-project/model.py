from pandas.core.algorithms import mode
from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, OrdinalEncoder
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from tabnet import TabNetClassifier, TabNetRegressor

def model_selection(model_name):
    if model_name == 'Ridge':
        model_test = Ridge()
    if model_name == 'Dummy':
        model_test = DummyRegressor(strategy='mean')
    if model_name == 'GradientBoostingRegressor':
        model_test = GradientBoostingRegressor(n_estimators=200, verbose=0, max_depth=5, learning_rate=0.05)
    if model_name == 'XGBRegressor':
        model_test = XGBRegressor(max_depth=10, n_estimators=300, learning_rate=0.05)
    if model_name == 'lightgbm':
        model_test = LGBMRegressor()
    if model_name == 'tabnet':
        model_test = TabNetRegressor()
    return model_test
