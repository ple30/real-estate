import pandas as pd
import openrouteservice

property_df = pd.read_csv("../data/raw/preprocessed properties.csv")

# If the API key not working please check README file for a new key
client = openrouteservice.Client(key='5b3ce3597851110001cf6248dc00320ff189425a87bb91f1d9b40af0')

def to_coordinates(address):
    try:
        geocode = client.pelias_search(text=address)
        if geocode and 'features' in geocode and len(geocode['features']) > 0:
            coordinates = geocode['features'][0]['geometry']['coordinates']
            latitude, longitude = coordinates[1], coordinates[0]
            return latitude, longitude 
    except:
        return None

property_df['full_address'] = property_df['address'] + ", " + property_df['suburb'] + ", " + property_df['postcode'].astype(str)
property_df[['latitude', 'longitude']] = property_df['full_address'].apply(lambda x: pd.Series(to_coordinates(x)))

property_df.to_csv("../data/raw/property_w_coordinates.csv", index=False)