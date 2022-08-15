import folium 
import pandas as pd
# from folium.plugins import MarketCluster
m = folium.Map(location=[48.86, 2.36], tiles = 'OpenStreetMap', zoom_start=5)
df = pd.read_csv('pub_data_with_lat_lng.csv')[['pub_name', 'address', 'lat', 'lng']]
df = df.drop_duplicates('pub_name', keep='first')

print(df)

for i, row in df.iterrows():
    lat = df.at[i, 'lat']
    lng = df.at[i, 'lng']
    pub = df.at[i, 'pub_name']

    popup = df.at[i, 'pub_name'] + '<br>' + str(df.at[i, 'address']) # <br> = linebreak

    folium.Marker(location=[lat,lng], popup=pub, icon=folium.Icon(color='blue')).add_to(m)
    print(i,"---DONE")

m.save('index.html')
df.to_csv('pub_location_data.csv')