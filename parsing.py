import pandas as pd

def parse_data(data):
    df = pd.read_excel(data)
    return df

def get_unique_values(df:pd.DataFrame, column:str) -> list:
    unique_values = []
    values = df[column].unique().tolist()
    return values

db = parse_data('DQGR_Verbatim_7-26-2023_15_38.xlsx')

positive_value = get_unique_values(db, '13. Positif_Themes')
negative_value = get_unique_values(db, '14. Negatif_Themes')

all_values = positive_value + negative_value
all_values_unique = list(set(all_values))

print(all_values_unique)