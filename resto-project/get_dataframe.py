from __main__ import max_depth, n_estimators, learning_rate, model_name
from __main__ import jour, service

model_name = model_name


def get_service(df, jour, service):
    df_jour = df[df['jour'] == jour]
    df_service = df_jour[df_jour['service'] == service]
    return df_service


def get_XY(df):
    X = df.drop(columns=["CA_TTC"])
    y = df.CA_TTC
    return X, y


if __name__ == '__main__':
    get_service()
    get_XY()
