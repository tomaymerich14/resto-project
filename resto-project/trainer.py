#UTILS
from collections import UserDict
from io import RawIOBase
import pandas as pd
import numpy as np
#MLFLOW
import mlflow
from mlflow.tracking import MlflowClient
from memoized_property import memoized_property

#SKLEARN
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split, cross_val_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import MinMaxScaler,RobustScaler, OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor, StackingRegressor
from sklearn.ensemble import VotingRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.dummy import DummyRegressor

MLFLOW_URI = 'https://mlflow.lewagon.co/'


class Trainer():
    def __init__(self, X, y, resto_name):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y
        # for MLFlow
        self.experiment_name = f"[FRA][PARIS][655] Resto_Project_{resto_name}"

    def set_pipeline(self, model):
        # set features
        feat_ordinal_dict = {
        'Clear': ['0',0,'sky is clear'],
        'Clouds': ['0', 0,'scattered clouds','few clouds','broken clouds','overcast clouds'],
        'Drizzle': ['0',0,'light intensity drizzle','drizzle','heavy intensity drizzle'],
        'Drizzle_and_Rain': ['0',0,'light intensity drizzle rain','rain and drizzle'],
        'Fog': ['0',0,'fog'],
        'Mist': ['0',0,'mist'],
        'Rain': ['0',0,'light rain','light intensity shower rain','moderate rain','heavy intensity rain'],
        'Thunderstorm': ['0',0,'proximity thunderstorm','thunderstorm','thunderstorm with light rain','thunderstorm with heavy rain']
        }


        feat_ordinal = sorted(feat_ordinal_dict.keys()) # sort alphabetically
        feat_ordinal_values_sorted = [feat_ordinal_dict[i] for i in feat_ordinal]
        #print(feat_ordinal_values_sorted)
        encoder_ordinal = OrdinalEncoder(
            categories=feat_ordinal_values_sorted,
            dtype= np.int64,
            handle_unknown="use_encoded_value",
            unknown_value=-1 # Considers unknown values as worse than "missing"
        )
        #print(encoder_ordinal)

        preproc_ordinal = make_pipeline(
            SimpleImputer(strategy="constant", fill_value="missing"),
            encoder_ordinal,
            RobustScaler()
        )

        categorical_features = [
            'date', 'jour', 'service', 'weather_main', 'weather_description',
            'Match Happening', 'Match Happening-CL', 'match_edf',
            'roland_garros', 'fashion_week'
        ]

        numerical_features = [
            'temp', 'feels_like', 'temp_min', 'temp_max', 'wind_speed', 'clouds_all'
        ]
        ordinal_features = [
            'Clear', 'Clouds', 'Drizzle', 'Drizzle and Rain', 'Fog', 'Mist', 'Rain',
            'Thunderstorm'
        ]

        #set preproc
        preproc_numerical = make_pipeline(KNNImputer(), RobustScaler())

        preproc_categorical = make_pipeline(
            SimpleImputer(strategy="constant", fill_value="missing"),
            OneHotEncoder(handle_unknown="ignore"))

        preproc = make_column_transformer((preproc_numerical, numerical_features),
                                        (preproc_categorical, categorical_features),
                                        (preproc_ordinal, ordinal_features),
                                        remainder="drop")

        #set pipe
        self.pipeline = make_pipeline(preproc, model)
        #print(self.pipeline)

    def run(self,model):
        self.set_pipeline(model)
        self.pipeline.fit(self.X, self.y)

        try:
            len(mlflow_params_name_1) > 0
        except NameError:
            pass
        else:
            if len(mlflow_params_name_1) > 0:
                return self.mlflow_log_param(mlflow_params_name_1,
                                             mlflow_params_value_1)

        try:
            len(mlflow_params_name_2) > 0
        except NameError:
            pass
        else:
            if len(mlflow_params_name_2) > 0:
                return self.mlflow_log_param(mlflow_params_name_2,
                                             mlflow_params_value_2)

        try:
            len(mlflow_params_name_3) > 0
        except NameError:
            pass
        else:
            if len(mlflow_params_name_3) > 0:
                return self.mlflow_log_param(mlflow_params_name_2,
                                             mlflow_params_value_2)



    def evaluate(self, X, y):
        pipe = self.pipeline
        r2_score = cross_val_score(pipe, X_d2, y_d2, cv=20).mean()
        self.mlflow_log_metric('r2_score', r2_score)



    # MLFlow methods
    @memoized_property
    def mlflow_client(self):
        mlflow.set_tracking_uri(MLFLOW_URI)
        return MlflowClient()

    @memoized_property
    def mlflow_experiment_id(self):
        try:
            return self.mlflow_client.create_experiment(self.experiment_name)
        except BaseException:
            return self.mlflow_client.get_experiment_by_name(
                self.experiment_name).experiment_id

    @memoized_property
    def mlflow_run(self):
        return self.mlflow_client.create_run(self.mlflow_experiment_id,
                                             tags=dict(hello=b"True"),
                                             UserDict=dict(hello=b"True"))

    def mlflow_log_param(self, key, value):
        self.mlflow_client.log_param(self.mlflow_run.info.run_id, key, value)

    def mlflow_log_metric(self, key, value):
        self.mlflow_client.log_metric(self.mlflow_run.info.run_id, key, value)


if __name__ == "__main__":

    preproc_data_d2=pd.read_csv('../raw_data/preproc_data_d2.csv')
    preproc_data_d16 = pd.read_csv('../raw_data/preproc_data_d16.csv')

    X_d2 = preproc_data_d2.drop(columns=["CA_TTC"])
    y_d2 = preproc_data_d2.CA_TTC
    X_d16 = preproc_data_d16.drop(columns=["CA_TTC"])
    y_d16 = preproc_data_d16.CA_TTC

    ###CHOOSE THE DATASET###
    dataset_test_D2 = True
    dataset_test_D16 = True

    ###CHOOSE THE MODEL###
    # -> possible models = 'Ridge', 'Dummy'
    model_name = 'Dummy'

    ###MLFLOW###
    from model import model_selection
    model_test = model_selection(model_name)

    ###CHOOSE MLF PARAMS###
    from model import mflflow_params

    mlflow_params_name_1 = mflflow_params(model_name)[0]
    mlflow_params_value_1 = mflflow_params(model_name)[1]
    ###
    mlflow_params_name_2 = ''
    mlflow_params_value_2 = ''
    ###
    mlflow_params_name_3 = ''
    mlflow_params_value_3 = ''

    ###RUN###
    if dataset_test_D2 == True:
        train_d2 = Trainer(X_d2, y_d2, dataset_test_D2)
        train_d2.run(model=model_test)
        train_d2.evaluate(X_d2, y_d2)

    if dataset_test_D16 == True:
        train_d16 = Trainer(X_d16, y_d16, dataset_test_D16)
        train_d16.run(model=model_test)
        train_d16.evaluate(X_d16, y_d16)
