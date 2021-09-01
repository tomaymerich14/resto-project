from process_raw_excel import *
from features_fi import *
from merge import *

def run():
    excel_to_csv('CA_DarocoBourse')
    excel_to_csv('CA_DarocoXVI')
    #features_fi()
    merge()
    pass
