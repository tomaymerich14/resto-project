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
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from xgboost import XGBRegressor
from sklearn.model_selection import RepeatedKFold

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
        self.experiment_name = f"[FRA][PARIS][655] Resto_Project_{resto_name}_COUV"

    def set_pipeline(self, model):
        # set features
        feat_ordinal_dict = {
            'clear': ['0', 0, 'sky is clear'],
            'clouds': [
                '0', 0, 'scattered clouds', 'few clouds', 'broken clouds',
                'overcast clouds'
            ],
            'drizzle': [
                '0', 0, 'light intensity drizzle', 'drizzle',
                'heavy intensity drizzle'
            ],
            'drizzle_and_rain':
            ['0', 0, 'light intensity drizzle rain', 'rain and drizzle'],
            'fog': ['0', 0, 'fog'],
            'mist': ['0', 0, 'mist'],
            'rain': [
                '0', 0, 'light rain', 'light intensity shower rain',
                'moderate rain', 'heavy intensity rain'
            ],
            'thunderstorm': [
                '0', 0, 'proximity thunderstorm', 'thunderstorm',
                'thunderstorm with light rain', 'thunderstorm with heavy rain'
            ]
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
        self.pipeline = Pipeline(steps=[('preproc', preproc), ('model',
                                                               model)])

    def run(self, model):
        self.set_pipeline(model)
        self.pipeline.fit(self.X, self.y)
        self.mlflow_log_param(mlflow_params_name_1, mlflow_params_value_1)
        self.mlflow_log_param(mlflow_params_name_2, mlflow_params_value_2)

    def evaluate(self, X, y):
        pipe = self.pipeline
        cv = RepeatedKFold(n_splits=5, n_repeats=2, random_state=0)
        y_pred = cross_val_score(pipe,
                                 X,
                                 y,
                                 cv=cv,
                                 scoring='neg_mean_absolute_error',
                                 n_jobs=-1)
        mae = np.mean(y_pred)
        std = np.std(y_pred)
        self.mlflow_log_metric('mae', mae)
        self.mlflow_log_metric('std', std)
        return y_pred

    def save_model_locally(self, path):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, path)
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


def preprocess_couv(df):
    '''function that preprocesses data couverts'''
    df = df.drop(columns='Restaurant')
    df['Jour'] = pd.to_datetime(df['Jour'], format='%Y-%m-%d')
    df = df[(df['Jour'] >= "2019-01-01") & (df['Jour'] <= "2021-07-31")]
    df = df.sort_values(by='Jour').reset_index(drop=True)
    df = df.rename(
        columns={
            "Jour": "date",
            "Service": "service",
            'Nombre de Réservations': 'nb_resa',
            'Nombre de couverts réservation': 'nb_couverts_resa',
            'Nombre de Passages': 'nb_passage',
            'Nombre de couverts passage': 'nb_couverts_passage',
            'Nombre de couverts total': 'total_couverts',
            'Délai en jour entre la prise de résa et le jour de résa':
            'temps_resa'
        })
    for i in range(len(df)):
        if df['service'][i] == 'Diner - ':
            df['service'][i] = 'soir'
        elif df['service'][i] == 'Dîner':
            df['service'][i] = 'soir'
        elif df['service'][i] == 'Dîner - ':
            df['service'][i] = 'soir'
        elif df['service'][i] == 'Diner - 2ème service':
            df['service'][i] = 'soir'
        elif df['service'][i] == 'Diner jo':
            df['service'][i] = 'soir'
        elif df['service'][i] == 'DINER JO':
            df['service'][i] = 'soir'
        elif df['service'][i] == 'Déjeuner':
            df['service'][i] = 'midi'
        elif df['service'][i] == 'Dejeuner':
            df['service'][i] = 'midi'
        elif df['service'][i] == 'Dejeuner week-end':
            df['service'][i] = 'midi'

    df = df.drop(df.loc[df['total_couverts'] <= 10].index)
    df = df.drop(columns=[
        'nb_resa', 'nb_couverts_resa', 'nb_passage', 'nb_couverts_passage',
        'temps_resa'
    ])

    return df


if __name__ == "__main__":


    # ----------------------PREPROCESSING DATA COUVERTS D2 & D16------------------------------------------------
    # ----------------------MERGE ON DATA CA----------------------------------------------------------------


    #-----------GET THE DATA-----------------------------------------
    preproc_data_d2 = pd.read_csv('../raw_data/preproc_data_d2.csv')
    preproc_data_d16 = pd.read_csv('../raw_data/preproc_data_d16.csv')

    df_d2_couv= pd.read_csv('../raw_data/export_d2.csv')
    df_d16_couv= pd.read_csv('../raw_data/export_d16.csv')
    #---------------------------------------------------------------



    #--------call function that preprocesses----
    df_d2_couv_preproc=preprocess_couv(df_d2_couv)
    df_d16_couv_preproc=preprocess_couv(df_d16_couv)
    #--------------------------------------------------


    #-----------------------------merge-------------------------------------
    preproc_data_d2['date'] = pd.to_datetime(preproc_data_d2['date'],
                                             format='%Y-%m-%d')
    preproc_data_d16['date'] = pd.to_datetime(preproc_data_d16['date'],
                                              format='%Y-%m-%d')


    preproc_merged_d2 = df_d2_couv_preproc.merge(preproc_data_d2,
                                                 how='inner',
                                                 left_on=['date', 'service'],
                                                 right_on=['date', 'service'])
    preproc_merged_d16 = df_d16_couv_preproc.merge(
        preproc_data_d16,
        how='inner',
        left_on=['date', 'service'],
        right_on=['date', 'service'])
    #--------------------------------------------------------------------


    #-----------------compute TICKET MOY to DROP outliers and absurd rows-------
    preproc_merged_d2['ticket_moy'] = preproc_merged_d2[
        'CA_TTC'] / preproc_merged_d2['total_couverts']

    preproc_merged_d2 = preproc_merged_d2.loc[
        (preproc_merged_d2['ticket_moy'] < 75)
        & (preproc_merged_d2['ticket_moy'] > 10)]

    preproc_merged_d16['ticket_moy'] = preproc_merged_d16[
        'CA_TTC'] / preproc_merged_d16['total_couverts']

    preproc_merged_d16 = preproc_merged_d16.loc[
        (preproc_merged_d16['ticket_moy'] < 75)
        & (preproc_merged_d16['ticket_moy'] > 5)]
    #--------------------------------------------------------------------


    #---------------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------------------


    def get_XY(df):
        X = df.drop(columns=["CA_TTC", 'ticket_moy','total_couverts'])
        y = df.total_couverts
        return X, y

    ### DAROCO BOURSE
    X_d2 = get_XY(preproc_merged_d2)[0]
    y_d2 = get_XY(preproc_merged_d2)[1]

    ### DAROCO 16
    X_d16 = get_XY(preproc_merged_d16)[0]
    y_d16 = get_XY(preproc_merged_d16)[1]

    t_d2 = Trainer(X_d2, y_d2, 'D2')

    ###CHOOSE THE DATASET###
    test_D2 = True
    test_D16 = True

    ###CHOOSE THE MODEL ###

    # go to model.py

    ### -> possible models =
    # 0:'RIDGE', 1:'DUMMY', 2:'GBR', 3:'XGB', 4:'LGBM', 5:'CATB'

    ###CHOOSE PARAMS###
    model_name = 'XGB'
    max_depth = [4, 3]
    n_estimators = [65, 60]
    learning_rate = [0.08, 0.08]

    model_test_D2 = XGBRegressor(max_depth=max_depth[0],
                                 n_estimators=n_estimators[0],
                                 learning_rate=learning_rate[0])
    model_test_D16 = XGBRegressor(max_depth=max_depth[1],
                                  n_estimators=n_estimators[1],
                                  learning_rate=learning_rate[1])

    ###GRIDSEARCH###
    allow_grid_search = False  #not working yet

    ###CHOOSE MLF PARAMS###
    from mlflow_params import get_params

    mlflow_params_name_1 = get_params(model_name)[0]
    mlflow_params_value_1 = get_params(model_name)[1]
    mlflow_params_name_2 = get_params(model_name)[2]
    mlflow_params_value_2 = get_params(model_name)[3]

    if test_D2 == True:
        resto_name = 'D2'
        train_d2 = Trainer(X_d2, y_d2, resto_name)
        train_d2.run(model=model_test_D2)
        train_d2.evaluate(X_d2, y_d2)
        train_d2.save_model_locally('../raw_data/model_d2_CO.joblib')

    if test_D16 == True:
        resto_name = 'D16'
        train_d16 = Trainer(X_d16, y_d16, resto_name)
        train_d16.run(model=model_test_D16)
        train_d16.evaluate(X_d16, y_d16)
        train_d16.save_model_locally('../raw_data/model_d16_CO.joblib')

    ###TO DO###

    #if allow_grid_search == True:
    #        self.pipeline = grid_search()[0]
    #else:
    #        self.set_pipeline(model)
