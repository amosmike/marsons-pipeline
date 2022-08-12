import pandas as pd
import requests
import json
import yaml

# Read pub data
pub_df = pd.read_csv("cleaned_data.csv")

print(pub_df)
# Get key
def geo_key(key='GeoKey.yaml'):

    with open(key, 'r') as t:
        key = yaml.safe_load(t)

    KEY = key['KEY']

    return KEY


key = geo_key()


# Stop requesting already received lat lngs
mapping = {}
pub_df['lat'] = None
pub_df['lng'] = None

# API Call and get longitude and latitude values
for i, row in pub_df.iterrows():
    try:
        address = str(row['address'])
        if address in mapping:
            lat = mapping[address][0]
            lng = mapping[address][1]
            pub_df.loc[i, 'lat'] = lat
            pub_df.loc[i, 'lng'] = lng
            print(f"{i}---{address}---REPEAT")  
        else:
            parameters = {
                "key": key,
                "location": address
            }

            response = requests.get(
                        'http://www.mapquestapi.com/geocoding/v1/address',
                        params=parameters)
            data = json.loads(response.text)['results']
            # print(data)

            lat = data[0]['locations'][0]['latLng']['lat']
            lng = data[0]['locations'][0]['latLng']['lng']
            pub_df.loc[i, 'lat'] = lat
            pub_df.loc[i, 'lng'] = lng

            mapping[address] = (lat, lng)

            print(f"{i}---{address}---DONE")

    except Exception as e:
        # print(e)
        pub_df.at[i, 'lat'] = 'N/A'
        pub_df.at[i, 'lng'] = 'N/A'
        print(f"{i}---{address}---NOT-FOUND")

# print(mapping)
# Save data to CSV with geodata
pub_df.to_csv('pub_data_with_lat_lng.csv')
