import os
import io
import sys
import json
import zipfile
import requests
import pandas as pd


def defined_postcode(query):

    url = 'https://api.postcodes.io/postcodes/{}'.format(query)

    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        data = data['result']
        postcode = data['postcode']
        lat = data['latitude']
        lon = data['longitude']
        print('Retreived Postcode: {}'.format(postcode))
    else:
        print('Postcode API returned: {}'.format(response.status_code))
        print('Exitting Process')
        sys.exit(0)

    return postcode, lat, lon


def random_postcode():

    url = 'https://api.postcodes.io/random/postcodes'

    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        data = data['result']
        postcode = data['postcode']
        lat = data['latitude']
        lon = data['longitude']
        print('Retreived Postcode: {}'.format(postcode))
    else:
        print('Postcode API returned: {}'.format(response.status_code))
        print('Exitting Process')
        sys.exit(0)

    return postcode, lat, lon


def api_call(query, loc, lat, lon, radius):
    data_path = './data/'+str(query)+str('_')+str(loc)
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    url = 'https://records-ws.nbnatlas.org/occurrences/index/download?reasonTypeId=10&q={}&fq=genus:{}&lat={}&lon={}&radius={}&qa=none'.format(
        query, query, lat, lon, radius
    )

    response = requests.get(url)

    if response.status_code == 200:
        print('API returned data | downloading {} within {}k from {}'.format(
            query, radius, loc))
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(data_path)
        filename = data_path+str('/data.csv')
        data = pd.read_csv(filename, header=0)
    else:
        print('API returned error {} for {} query near {}'.format(
            response.status_code, query, loc))
        data = pd.DataFrame()

    return data


def get_data(loc, lat, lon, rad):

    fox = api_call(query='Vulpes', loc=loc,
                   lat=lat, lon=lon, radius=rad)

    cat = api_call(query='Felis', loc=loc,
                   lat=lat, lon=lon, radius=rad)

    hedgehog = api_call(query='Erinaceus', loc=loc,
                        lat=lat, lon=lon, radius=rad)

    badger = api_call(query='Meles', loc=loc,
                      lat=lat, lon=lon, radius=rad)

    roe = api_call(query='Capreolus', loc=loc,
                   lat=lat, lon=lon, radius=rad)

    deer = api_call(query='Cervus', loc=loc,
                    lat=lat, lon=lon, radius=rad)

    hare = api_call(query='Lepus', loc=loc,
                    lat=lat, lon=lon, radius=rad)

    rabbit = api_call(query='Oryctolagus', loc=loc,
                      lat=lat, lon=lon, radius=rad)

    squirrel = api_call(query='Sciurus', loc=loc,
                        lat=lat, lon=lon, radius=rad)

    animal_lst = [fox, cat, hedgehog, badger,
                  roe, deer, hare, rabbit, squirrel]

    data = pd.concat(animal_lst, axis=0, ignore_index=True, sort=False)

    #filename = './data/{}_sightings_10km.csv'.format(loc)

    #data.to_csv(filename, index=False)

    return data


def defined_areas():
    # Central Edinburgh EH1 3EG #Waverley
    # Central Glasgow G1 3SL #Central Station
    # Inverness Academy IV2 3PY #Central Station
    # Central Bristol BS1 2AN #Old City Walls
    # Norwich NR1 1EF
    # Leeds LS1 4DY
    # Cardiff CF10 1EP

    # National Parks
    # Cairngorms National Park PH26 3HG
    # Hellvellyn Peak Lake District CA11 0PU
    # Snowdonia National Park LL48 6LF
    # South Downs National Park GU29 9DH
    # New Forest National Park Lyndhurst SO43 7BJ

    postcodes = ['PH26 3HG', 'CA11 0PU', 'LL48 6LF', 'GU29 9DH', 'SO43 7BJ']
    national_park = ['Cairngorms', 'Lake District',
                     'Snowdonia', 'South Downs', 'New Forest']

    for i in range(len(postcodes)):
        print('################################')
        postcode, lat, lon = defined_postcode(query=postcodes[i])

        get_data(loc=national_park[i], lat=lat, lon=lon)
        print('################################')


def rand_postcode():

    postcode, lat, lon = random_postcode()
    get_data(loc=postcode, lat=lat, lon=lon, rad=10.0)


def postcode_findr(lookup):

    postcode, lat, lon = defined_postcode(query=lookup)
    data = get_data(loc=postcode, lat=lat, lon=lon, rad=10.0)

    return data
