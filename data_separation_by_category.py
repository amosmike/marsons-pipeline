import pandas as pd

df = pd.read_csv('pub_data_with_lat_lng.csv')[['Unnamed: 0','pub_name','address','category','item_name','item_price','opening_times','lat','lng']]
df.dropna(inplace=True)

df_starters = df[df['category'].str.contains("Starters & Sharers")]
df_starters.to_csv('dataframes/df_starters.csv')

df_burgers = df[df['category'].str.contains("Burgers")]
df_burgers.to_csv('dataframes/df_burgers.csv')

df_draught = df[df['category'].str.contains("Draught")] 
df_draught.to_csv('dataframes/df_draught.csv')

df_soft = df[df['category'].str.contains("Soft Drinks")] 
df_soft.to_csv('dataframes/df_soft.csv')

df_desserts = df[df['category'].str.contains("Desserts")] 
df_desserts.to_csv('dataframes/df_desserts.csv')

df_wine = df[df['category'].str.contains("Wine")] 
df_wine.to_csv('dataframes/df_wine.csv')


