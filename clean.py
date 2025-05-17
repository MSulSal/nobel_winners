import pandas as pd
import numpy as np
import sqlalchemy

engine = sqlalchemy.create_engine("sqlite:///data/nobel_winners_clean.db")


df = pd.read_json("data/nwinners.json")

def parse_date_flexible(date_str):
    try:
        return pd.to_datetime(date_str, errors='raise')
    except:
        # Handle year-only dates
        if date_str.isdigit() and len(date_str) == 4:
            return pd.to_datetime(f"{date_str}-01-01")
        else:
            return pd.NaT

def clean_data(df):
    # normalize empty strings with NaN
    df.replace("", np.nan, inplace=True)
    # remove asterisks and white space
    df.name = df.name.str.replace("*", "", regex=False).str.strip()
    # remove born_in column
    df_born_in = df[df.born_in.notnull()]
    df = df[df.born_in.isnull()].drop("born_in", axis=1)
    # remove duplicates
    df.loc[(df.name == 'Marie Sk\u0142odowska-Curie') & (df.year == 1911), 'country'] = 'France'
    df.drop(df[(df.name == 'Sidney Altman') & (df.year == 1990)].index,
inplace=True)
    # remove rows with year < 1901
    df = df[df.year >= 1901]
    # shuffle and drop duplicate countries randomly
    df = df.reindex(np.random.permutation(df.index))
    df = df.drop_duplicates(["name", "year"])
    df = df.sort_index()
    # standardize datetime
    df["date_of_birth"] = df["date_of_birth"].apply(parse_date_flexible)
    df["date_of_death"] = df["date_of_death"].apply(parse_date_flexible)
    df["award_age"] = df.year - pd.DatetimeIndex(df.date_of_birth).year
    
    return df, df_born_in

df_clean, df_born_in = clean_data(df)
df_born_in.name = df_born_in.name.str.replace("*", "", regex=False)
df_born_in.name = df_born_in.name.str.strip()
df_born_in.drop_duplicates(subset=['name'], inplace=True)
df_born_in.set_index('name', inplace=True)

def get_born_in(name):
    try:
        born_in = df_born_in.loc[name]["born_in"]
        # print('name: %s, born in: %s'%(name, born_in))
    except:
        born_in = np.nan
    return born_in

df_wbi = df_clean.copy()
df_wbi['born_in'] = df_wbi['name'].apply(get_born_in)

# read the Scrapy bio-data into a DataFrame
df_winners_bios = pd.read_json("data/minibio.json")
df_clean_bios = pd.merge(df_wbi, df_winners_bios, how='outer', on='link')
# drop duplicate rows
df_clean_bios = df_clean_bios[~df_clean_bios.name.isnull()].drop_duplicates(subset=['link', 'year'])

# assume df_clean_bios['image_urls'] contains lists like ['url1','url2',…]
df_clean_bios['image_urls'] = df_clean_bios['image_urls'].str.join(';')


df_clean_bios.to_json('data/nobel_winners_cleaned.json', orient='records', date_format='iso')
df_clean_bios.to_sql("winners", engine, if_exists="replace")
df_read_sql = pd.read_sql("winners", engine)