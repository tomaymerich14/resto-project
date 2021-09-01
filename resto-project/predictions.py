#UTILS
import pandas as pd
import numpy as np
#MLFLOW
import mlflow
from mlflow.tracking import MlflowClient
from memoized_property import memoized_property

#JOBLIB
import joblib
from termcolor import colored

#SKLEARN
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from xgboost import XGBRegressor
from sklearn.model_selection import RepeatedKFold

############# IMPORT OUR TEST DATA #############
test_d2 = pd.read_csv('../raw_data/forecasted_services_d2.csv')
test_d16 = pd.read_csv('../raw_data/forecasted_services_d16.csv')

############  DEFINE THE MODELS ################
model_name = 'XGB'
max_depth = [4,3]
n_estimators = [65,60]
learning_rate = [0.08,0.08]

model_test_D2 = XGBRegressor(max_depth=max_depth[0],
                            n_estimators=n_estimators[0],
                            learning_rate=learning_rate[0])
model_test_D16 = XGBRegressor(max_depth=max_depth[1],
                            n_estimators=n_estimators[1],
                            learning_rate=learning_rate[1])
