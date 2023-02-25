import pandas as pd
import os

version = len(os.listdir("file_version_control"))
df = pd.read_parquet('milano_housing_price_clean.parquet.gzip', engine='fastparquet')
df.to_excel(f'file_version_control/milano_housing_{version+1}.xlsx', engine='xlsxwriter')


#%%
