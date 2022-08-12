import folium 
import pandas as pd
# from folium.plugins import MarketCluster
m = folium.Map(location=[48.86, 2.36], tiles = 'OpenStreetMap', zoom_start=5)
df = pd.read_csv('pub_data_with_lat_lng.csv')

mapping = {}
df['lat'] = None
df['lng'] = None

for i, row in df[:50].iterrows():
    try:
        pub = str(row['pub_name'])
        if pub in mapping:
            # lat = mapping[pub][0]
            # lng = mapping[pub][1]
            print("passed")
            pass
        else:
            lat = df.at[i, 'lat']
            lng = df.at[i, 'lng']
            pub = df.at[i, 'pub_name']
            popup = df.at[i, 'pub_name'] + '<br>' + str(df.at[i, 'address']) # <br> = linebreak
            folium.Marker(location=[lat,lng], popup=pub, icon=folium.Icon(color='blue')).add_to(m)
            mapping[pub] = (lat, lng)
            print("new")
    except:
        print("error")
        pass
    
m.save('index.html')