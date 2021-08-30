import pandas as pd
set_d2 = pd.read_csv('../raw_data/df_feat_d2.csv')
set_d16= pd.read_csv('../raw_data/df_feat_d16.csv')
index_d2 = ['Daroco Bourse']
index_d16 = ['Daroco 16']
def actual_chiffres():
    prov_actual_dict_d2 = {}
    prov_actual_dict_d16 = {}
    for i in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']:
        set_d2_series = set_d2[set_d2['jour']==i]
        set_d16_series = set_d16[set_d16['jour']==i]
        prov_actual_dict_d2[i]=set_d2_series['CA_TTC'].mean()
        prov_actual_dict_d16[i]=set_d16_series['CA_TTC'].mean()
    for i in ['soir','midi']:
        set_d2_series = set_d2[set_d2['service']==i]
        set_d16_series = set_d16[set_d16['service']==i]
        prov_actual_dict_d2[i]=set_d2_series['CA_TTC'].mean()
        prov_actual_dict_d16[i]=set_d16_series['CA_TTC'].mean()
    for y in ['soir','midi']:
        for i in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']:
            set_d2_series = set_d2[(set_d2['jour']==i) & (set_d2['service']==y)]
            set_d16_series = set_d16[(set_d16['jour']==i) & (set_d16['service']==y)]

            prov_actual_dict_d2[f'{i} {y}']=set_d2_series['CA_TTC'].mean()
            prov_actual_dict_d16[f'{i} {y}']=set_d16_series['CA_TTC'].mean()

    prov_actual_dict_d2 = pd.DataFrame(data=prov_actual_dict_d2, index=index_d2)
    prov_actual_dict_d2.to_csv('../raw_data/CA_d2.csv')

    prov_actual_dict_d16 = pd.DataFrame(data=prov_actual_dict_d16, index=index_d16)
    prov_actual_dict_d16.to_csv('../raw_data/CA_d16.csv')

if __name__=='__main__':
    actual_chiffres()
