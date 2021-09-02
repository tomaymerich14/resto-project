import pandas as pd
import joblib

def column_order_couvert():
    pipeline_couvert_d2 = joblib.load('../joblibs/model_d2_CO.joblib')

    df2=pd.read_csv('../raw_data/forecasted_services_d2.csv')
    df2=df2[list(list(pipeline_couvert_d2)[0]._df_columns)]
    df2.to_csv('../raw_data/forecasted_services_d2.csv', index=False)

    df16=pd.read_csv('../raw_data/forecasted_services_d16.csv')
    df16=df16[list(list(pipeline_couvert_d2)[0]._df_columns)]
    df16.to_csv('../raw_data/forecasted_services_d16.csv', index=False)

if __name__=='__main__':
    column_order_couvert()
