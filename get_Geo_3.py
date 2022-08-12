import pandas as pd
import requests
import json
import yaml

# Read pub data
pub_df = pd.read_csv("cleaned_data.csv")

# Get key
def geo_key(key = 'GeoKey.yaml'): 

    with open(key, 'r') as t:
        key = yaml.safe_load(t)

    KEY = key['KEY']

    return KEY

key = geo_key()


# Stop requesting already received lat lngs
mapping_address = []
mapping_lat = []
mapping_lng = []

# API Call and get longitude and latitude values
for i, row in pub_df[:3].iterrows():
    try: 
        apiAddress = str(pub_df.at[i,'address'])
        # print(apiAddress)
        parameters = {
            "key" : key,
            "location" : apiAddress
        }
        for c1, c2, c3 in zip(mapping_address, mapping_lat, mapping_lng):        
            if c1 not in mapping_address:
                response = requests.get('http://www.mapquestapi.com/geocoding/v1/address', params = parameters)
                # print(response.text)
                data = json.loads(response.text)['results']

                lat = data[0]['locations'][0]['latLng']['lat']
                lng = data[0]['locations'][0]['latLng']['lng']

                pub_df.at[i,'lat'] = lat
                pub_df.at[i,'lng'] = lng

                mapping_address.append(apiAddress)
                mapping_lat.append(lat)
                mapping_lng.append(lng)

                print(f"{i}---{apiAddress}---DONE")
            else:
                pub_df.at[i,'lat'] = c2
                pub_df.at[i,'lng'] = c3
                print(f"{i}---{apiAddress}---REPEAT")

    except:
        pub_df.at[i,'lat'] = 'N/A'
        pub_df.at[i,'lng'] = 'N/A'
        print(f"{i}---{apiAddress}---NOT-FOUND")


# Save data to CSV with geodata
pub_df.to_csv('pub_data_with_lat_lng.csv')