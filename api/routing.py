from itertools import product

import requests
import json
import pandas as pd

from api import config
import datetime


def query(startingTime, origin_location, dest_location, transport_mode='publicTransport', route_type='fastest',
          time_type='depart'):
    querystring = {"apikey": config.APIKEY,
                   "locations": f'{origin_location[0]},{origin_location[1]}:{dest_location[0]},{dest_location[1]}',
                   "language": config.LANG,
                   "dateTime": startingTime,
                   "timeType": time_type if time_type in config.OPTIONS['timeType'] else "depart",
                   "instructions": "true",
                   "polyline": "true",
                   "routeType": route_type if route_type in config.OPTIONS['routeType'] else "fastest",
                   # "avoidPublicTransportTypes": "ferry",
                   # "avoid": "tollRoads",
                   "transportMode": transport_mode if transport_mode in config.OPTIONS[
                       'transportMode'] else 'publicTransport',
                   "maxAlternatives": "1"}

    response = requests.request("GET", config.URL, data="", headers=config.HEADERS, params=querystring)
    result = json.loads(response.text)
    if len(result['routes']) == 1:
        return result['routes'][0]['summary'], result['routes'][0]['legs']
    return [(x['summary'], x['legs']) for x in result['routes']]


def query_duration(startingTime, origin_location, dest_location, transport_mode='publicTransport', route_type='fastest',
                   time_type='depart'):
    querystring = {"apikey": config.APIKEY,
                   "locations": f'{origin_location[0]},{origin_location[1]}:{dest_location[0]},{dest_location[1]}',
                   "language": config.LANG,
                   "dateTime": startingTime,
                   "timeType": time_type if time_type in config.OPTIONS['timeType'] else "depart",
                   "instructions": "true",
                   "polyline": "true",
                   "routeType": route_type if route_type in config.OPTIONS['routeType'] else "fastest",
                   # "avoidPublicTransportTypes": "ferry",
                   # "avoid": "tollRoads",
                   "transportMode": transport_mode if transport_mode in config.OPTIONS[
                       'transportMode'] else 'publicTransport',
                   "maxAlternatives": "1"}

    response = requests.request("GET", config.URL, data="", headers=config.HEADERS, params=querystring)
    result = json.loads(response.text)
    if 'routes' not in result:
        return -1
    if len(result['routes']) == 1:
        return result['routes'][0]['summary']['duration']
    return [x['summary']['duration'] for x in result['routes']]


def get_all_combinations(csv_file, startingDate, increment=900):
    df = pd.read_csv(csv_file)
    combs = pd.DataFrame(list(product(df.values, df.values)), columns=['l1', 'l2'])
    a = datetime.datetime.strptime(startingDate, '%Y-%m-%dT%H:%M:%S')
    b = datetime.datetime.strptime(startingDate, '%Y-%m-%dT%H:%M:%S')
    f = open('../durations.csv', 'w')
    f.write('Date, Origin, Destination, Duration\n')

    while a.date() == b.date():

        for i in range(len(combs)):
            row = combs.iloc[i].values
            if row[0][0] == row[1][0]:
                continue
            d = b.strftime('%Y-%m-%dT%H:%M:%S')
            dur = query_duration(d, row[0][1:3], row[1][1:3])
            f.write(f'{d},{row[0][0]},{row[1][0]},{dur}\n')
            f.flush()
        b = b + datetime.timedelta(0, increment)


if __name__ == '__main__':
    # print(query('2018-11-17T19:20:00', [52.1145, 4.2790], [52.0995, 4.2969]))
    get_all_combinations('../locations.csv', '2018-11-17T08:00:00')
