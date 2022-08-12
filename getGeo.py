import pandas as pd
import requests
import json

# Read pub data
pub_df = pd.read_csv("cleaned_data.csv")

# API Call and get longitude and latitude values
for i, row in pub_df[:3].iterrows():
    try: 
        apiAddress = str(pub_df.at[i,'address'])
        # print(apiAddress)
        parameters = {
            "key" : "yNmCgGiEia8EFfLSJKswsphu2WCwl3HG",
            "location" : apiAddress
        }

        response = requests.get('http://www.mapquestapi.com/geocoding/v1/address', params = parameters)
        # print(response.text)
        data = json.loads(response.text)['results']

        lat = data[0]['locations'][0]['latLng']['lat']
        lng = data[0]['locations'][0]['latLng']['lng']

        pub_df.at[i,'lat'] = lat
        pub_df.at[i,'lng'] = lng

        print(f"{i}---{apiAddress}---DONE")
    except:
        pub_df.at[i,'lat'] = 'N/A'
        pub_df.at[i,'lng'] = 'N/A'
        print(f"{i}---{apiAddress}---NOT-FOUND")


# Save data to CSV with geodata
pub_df.to_csv('pub_data_with_lat_lng.csv')