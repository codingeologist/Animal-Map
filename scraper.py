import os
import io
import sys
import json
import zipfile
import requests
import pandas as pd


def defined_postcode(query):

    url = "https://api.postcodes.io/postcodes/{}".format(query)

    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        data = data["result"]
        postcode = data["postcode"]
        lat = data["latitude"]
        lon = data["longitude"]
        print("Retreived Postcode: {}".format(postcode))
    else:
        print("Postcode API returned: {}".format(response.status_code))
        print("Exitting Process")
        sys.exit(0)

    return postcode, lat, lon


def random_postcode():

    url = "https://api.postcodes.io/random/postcodes"

    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        data = data["result"]
        postcode = data["postcode"]
        lat = data["latitude"]
        lon = data["longitude"]
        print("Retreived Postcode: {}".format(postcode))
    else:
        print("Postcode API returned: {}".format(response.status_code))
        print("Exitting Process")
        sys.exit(0)

    return postcode, lat, lon


def api_call(query, loc, lat, lon, radius):

    start_index = 0
    url = "https://records-ws.nbnatlas.org/occurrences/search?q={}&fq=genus:{}&lat={}&lon={}&radius=10.0".format(
        query, query, lat, lon, radius
    )

    columns = [
        "uuid",
        "speciesGuid",
        "scientificName",
        "vernacularName",
        "taxonRank",
        "stateProvince",
        "country",
        "decimalLatitude",
        "decimalLongitude"
    ]

    occurrences = []
    
    while True:
        response = requests.get(f"{url}&startIndex={start_index}&pageSize=100")

        if response.status_code != 200:
            # print("API returned error {} for {} query near {}".format(
            #     response.status_code, query, loc))
            data = pd.DataFrame(columns=columns)
            break
        
        new_occurrences = response.json()["occurrences"]
        occurrences.extend(new_occurrences)
        total_records = int(response.json()["totalRecords"])
        # print(f"query: {query}: start_index: {start_index} occurrences: {len(occurrences)}")

        if len(occurrences) >= total_records:
            break

        start_index += 100

    try:
        data = pd.json_normalize(occurrences)
        data = data[columns]
        return data
    except Exception:
        # print(f"No data returned by API")
        return pd.DataFrame(columns=columns)


def get_data(loc, lat, lon, rad):

    fox = api_call(query="Vulpes", loc=loc,
                   lat=lat, lon=lon, radius=rad)

    cat = api_call(query="Felis", loc=loc,
                   lat=lat, lon=lon, radius=rad)

    hedgehog = api_call(query="Erinaceus", loc=loc,
                        lat=lat, lon=lon, radius=rad)

    badger = api_call(query="Meles", loc=loc,
                      lat=lat, lon=lon, radius=rad)

    roe = api_call(query="Capreolus", loc=loc,
                   lat=lat, lon=lon, radius=rad)

    deer = api_call(query="Cervus", loc=loc,
                    lat=lat, lon=lon, radius=rad)

    hare = api_call(query="Lepus", loc=loc,
                    lat=lat, lon=lon, radius=rad)

    rabbit = api_call(query="Oryctolagus", loc=loc,
                      lat=lat, lon=lon, radius=rad)

    squirrel = api_call(query="Sciurus", loc=loc,
                        lat=lat, lon=lon, radius=rad)

    animal_lst = [fox, cat, hedgehog, badger,
                  roe, deer, hare, rabbit, squirrel]

    animal_lst = [df for df in animal_lst if not df.empty]

    data = pd.concat(animal_lst, axis=0, ignore_index=True, sort=False)

    return data


def defined_areas():

    postcodes = ["PH26 3HG", "CA11 0PU", "LL48 6LF", "GU29 9DH", "SO43 7BJ"]
    national_park = ["Cairngorms", "Lake District",
                     "Snowdonia", "South Downs", "New Forest"]

    for i in range(len(postcodes)):
        print("################################")
        postcode, lat, lon = defined_postcode(query=postcodes[i])

        get_data(loc=national_park[i], lat=lat, lon=lon)
        print("################################")


def rand_postcode():

    postcode, lat, lon = random_postcode()
    data = get_data(loc=postcode, lat=lat, lon=lon, rad=10.0)

    return data


def postcode_findr(lookup):

    postcode, lat, lon = defined_postcode(query=lookup)
    data = get_data(loc=postcode, lat=lat, lon=lon, rad=10.0)

    return data
