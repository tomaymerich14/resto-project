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
            'clear': ['0', 0, 'sky is clear'],
            'clouds': ['0', 0, 'scattered clouds', 'few clouds', 'broken clouds','overcast clouds'],
            'drizzle': ['0', 0, 'light intensity drizzle', 'drizzle','heavy intensity drizzle'],
            'drizzle_and_rain':['0', 0, 'light intensity drizzle rain', 'rain and drizzle'],
            'fog': ['0', 0, 'fog'],
            'mist': ['0', 0, 'mist'],
            'rain': ['0', 0, 'light rain', 'light intensity shower rain','moderate rain', 'heavy intensity rain'],
            'thunderstorm': ['0', 0, 'proximity thunderstorm', 'thunderstorm','thunderstorm with light rain', 'thunderstorm with heavy rain']
        }

        feat_ordinal = sorted(feat_ordinal_dict.keys())  # sort alphabetically
        feat_ordinal_values_sorted = [
            feat_ordinal_dict[i] for i in feat_ordinal
        ]
        #print(feat_ordinal_values_sorted)
        encoder_ordinal = OrdinalEncoder(
            categories=feat_ordinal_values_sorted,
            dtype=np.int64,
            handle_unknown="use_encoded_value",
            unknown_value=-1  # Considers unknown values as worse than "missing"
        )
        #print(encoder_ordinal)

        preproc_ordinal = make_pipeline(
            SimpleImputer(strategy="constant", fill_value="missing"),
            encoder_ordinal, RobustScaler())

        categorical_features = [
            'date', 'jour', 'service', 'match_happening', 'match_happening_cl',
            'match_edf', 'roland_garros', 'fashion_week', 'vacances_paris'
        ]
        cyclical_features = [
            'cos_jour_de_sem', 'sin_jour_de_sem', 'cos_jour_du_mois',
            'sin_jour_du_mois', 'cos_mois_de_annee', 'sin_mois_de_annee',
            'cos_jour_annee', 'sin_jour_annee', 'cos_semaine_annee',
            'sin_semaine_annee'
        ]
        numerical_features = [
            'moyen_7_services', 'moyen_31_services', 'moyenne_3der_j&service',
            'temp', 'feels_like', 'temp_min', 'temp_max', 'wind_speed',
            'clouds_all'
        ]
        ordinal_features = [
            'clear', 'clouds', 'drizzle', 'drizzle_and_rain', 'fog', 'mist',
            'rain', 'thunderstorm'
        ]

        #set preproc
        preproc_categorical = make_pipeline(
            SimpleImputer(strategy="constant", fill_value="missing"),
            OneHotEncoder(handle_unknown="ignore"))

        preproc_cyclical = make_pipeline(KNNImputer())

        preproc_numerical = make_pipeline(KNNImputer(), RobustScaler())

        preproc = make_column_transformer(
            (preproc_categorical, categorical_features),
            (preproc_cyclical, cyclical_features),
            (preproc_numerical, numerical_features),
            (preproc_ordinal, ordinal_features),
            remainder="drop")

        #set pipe
        self.pipeline = make_pipeline(preproc, model)

    def run(self, model):
        self.set_pipeline(model)
        self.pipeline.fit(self.X, self.y)
        self.mlflow_log_param(mlflow_params_name_1, mlflow_params_value_1)
        self.mlflow_log_param(mlflow_params_name_2, mlflow_params_value_2)

    def evaluate(self, X, y):
        pipe = self.pipeline
        y_pred = cross_val_score(pipe, X, y, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
        mae = np.mean(y_pred)
        std = np.std(y_pred)
        self.mlflow_log_metric('mae', mae)
        self.mlflow_log_metric('std', std)
        return y_pred

    def save_model_locally(self):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, 'model.joblib')
        print(colored("model.joblib saved locally", "green"))

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
        return self.mlflow_client.create_run(self.mlflow_experiment_id)
        #tags=dict(hello=b"True")

    def mlflow_log_param(self, key, value):
        self.mlflow_client.log_param(self.mlflow_run.info.run_id, key, value)

    def mlflow_log_metric(self, key, value):
        self.mlflow_client.log_metric(self.mlflow_run.info.run_id, key, value)


if __name__ == "__main__":

    preproc_data_d2 = pd.read_csv('../raw_data/preproc_data_d2.csv')
    preproc_data_d16 = pd.read_csv('../raw_data/preproc_data_d16.csv')

    from get_dataframe import get_XY

    X_d2 = get_XY(preproc_data_d2)[0]
    y_d2 = get_XY(preproc_data_d2)[1]
    X_d16 = get_XY(preproc_data_d16)[0]
    y_d16 = get_XY(preproc_data_d16)[1]


    ###CHOOSE THE DATASET###
    test_D2 = True
    test_D16 = True

    ###CHOOSE THE MODEL ###
    from model import model_selection

    # go to model.py

    ### -> possible models =
    # 0:'RIDGE', 1:'DUMMY', 2:'GBR', 3:'XGB', 4:'LGBM', 5:'CATB'

    ###CHOOSE PARAMS###
    model_name = 'XGB'
    max_depth = 4
    n_estimators = 200
    learning_rate = 0.1

    model_test = model_selection(model_name)


    ###GRIDSEARCH###
    allow_grid_search = False #not working yet

    ###CHOOSE MLF PARAMS###
    from mlflow_params import get_params

    mlflow_params_name_1 = get_params(model_name)[0]
    mlflow_params_value_1 = get_params(model_name)[1]
    mlflow_params_name_2 = get_params(model_name)[2]
    mlflow_params_value_2 = get_params(model_name)[3]

    if test_D2 == True:
        resto_name = 'D2'
        train_d2 = Trainer(X_d2, y_d2, resto_name)
        train_d2.run(model=model_test)
        train_d2.evaluate(X_d2, y_d2)

    if test_D16 == True:
        resto_name = 'D16'
        train_d16 = Trainer(X_d16, y_d16, resto_name)
        train_d16.run(model=model_test)
        train_d16.evaluate(X_d16, y_d16)

    ###TO DO###

    #if allow_grid_search == True:
    #        self.pipeline = grid_search()[0]
    #else:
    #        self.set_pipeline(model)
