#enter df = X_d16, X_d2
#enter jour = 'Lundi', 'Mardi' , ...
#enter service = 'soir, 'midi'


def get_service(df, jour, service):
    df_jour = df[df['jour'] == jour]
    df_service = df_jour[df_jour['service'] == service]
    return df_service


def get_XY(df):
    X = df.drop(columns=["CA_TTC"])
    y = df.CA_TTC
    return X, y
