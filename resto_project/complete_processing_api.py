from process_data import jour_annee, fetch_data_api, process_api_forecast
from test_cyclical import cyclical_columns
from column_order_couvert import column_order_couvert
from column_order_CA import column_order_CA

if __name__ == '__main__':
    process_api_forecast()
    cyclical_columns()
    column_order_couvert()
    column_order_CA()
