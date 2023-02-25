import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

def upload_data():
    df = pd.read_parquet('milano_housing_price.parquet.gzip', engine='fastparquet')
    df.columns = ['price', 'rooms', 'm2', 'bathrooms', 'floor', 'description',
                  'condominium_expenses', 'energy_class', 'date',
                  'contract', 'typology', 'surface', 'rooms2', 'floor2',
                  'total_floors', 'availability', 'other_features',
                  'price2', 'condominium_expenses2', 'year_of_build', 'condition',
                  'heating', 'air_conditioning', 'energy_efficiency', 'city',
                  'neighborhood', 'address', 'href', 'car_parking',
                  'renewable_energy_performance_index',
                  'energy_performance_building', 'housing units',
                  'start_end_works', 'current_building_use',
                  'energy_certification', 'co2_emissions']
    return df


def clean_data(df):
    df['price'] = df['price'].str.replace('€', '')
    df['price'] = df['price'].apply(lambda x: x.split('-')[0] if x else x)

    df['m2'] = df['m2'].str.replace(r'\D', '')

    df['bathrooms'] = df['bathrooms'].apply(lambda x: np.nan if x and "€" in x else x)
    df['floor'] = df['floor'].apply(lambda x: np.nan if x and "€" in x else x)

    df['prezzo'], df['condominium_expenses'] = df['condominium_expenses'].str.split('condominio€ ', 1).str
    df['condominium_expenses'] = df['condominium_expenses'].str.replace('/mese', '')
    df.drop(columns=['prezzo'])

    date_regex = r'(\d{2}/\d{2}/\d{4})'
    df['date'] = df['date'].str.extract(date_regex)

    df['elevator'] = df['floor2'].apply(lambda x: 1 if x and "ascensore" in x else 0)
    df['floor_level'] = df['floor2'].apply(lambda x: x[0] if x else x)
    df['floor_level'] = df['floor_level'].str.replace('P', '0')

    df['other_features'].unique()

    df['heating_centralized'], df['heating_radiator'], df['heating_gas'] = df['heating'].str.split(',', 2).str

    df['air_conditiong_centralized'], df['air_conditioning_heat'] = df['air_conditioning'].str.split(',', 1).str

    df['renewable_energy_performance_index_KWh/m2'] = df['renewable_energy_performance_index'].str.replace(r'\D', '')

    df['housing units'] = df['housing units'].str.replace(r'\D', '')

    columns_to_drop = ['price2', 'surface', 'renewable_energy_performance_index',
                       'rooms2', 'description', 'address']

    df.drop(columns=columns_to_drop, inplace=True)
    return df

def create_clean_data(df):
    df.to_csv('milano_housing_price_clean.csv', index=False)
    df.to_parquet('milano_housing_price_clean.parquet.gzip', engine='fastparquet')
    print('data cleaned and saved')

# main
def main():
    df = upload_data()
    df = clean_data(df)
    create_clean_data(df)

#%%
