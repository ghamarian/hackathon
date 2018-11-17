from itertools import product

import requests
import json
import pandas as pd

from api import config
import datetime

import datetime
import itertools

all_site_ls = [
    "centraal",
    "maduradam",
    "gemeentemuseume",
    "kijkduin",
    "de uithof",
    "haagsemarkt",
    "mauritshuis",
    "familiepark drievliet",
    "huistenbosch",
    "Museum Voorlinden",
    "scheveningen"
]
site2duration = dict.fromkeys(all_site_ls, 60 * 60 * 0.75
                              )

starting_location = 'centraal'
site2duration['gemeentemuseume'] = 60 * 60 * 2
site2duration['familiepark drievliet'] = 60 * 60 * 1
site2duration['kijkduin'] = 60 * 60 * 1


def compute_all_itineraries_duration(ddf, site2duration, starting_location, starting_time, sites_to_visit_ls, ):
    starting_time = pd.to_datetime(starting_time)
    path2time_duration = {}  # pd.Series()
    path2end_time = {}  # pd.Series()
    path2step2dep_time = {}


    for iItinerary_tuple in itertools.permutations(sites_to_visit_ls):
        tmp_full_itinerary_ls = [starting_location] + list(iItinerary_tuple)
        tmp_step_starting_time = starting_time  # pd.to_datetime(starting_time)
        # tmp_itinerary_time_duration = 0
        #         tmp_step2dep_time = {}
        tmp_step_time_ls = []
        tmp_step_time_duration = -1
        for jFirst_site, jSecond_site in zip(tmp_full_itinerary_ls, tmp_full_itinerary_ls[1:]):
            tmp_current_from_to_ddf = ddf.query(
                'Date >= @tmp_step_starting_time and Origin == @jFirst_site and Destination == @jSecond_site')
            if tmp_current_from_to_ddf.empty:
                tmp_step_time_duration = -1
                #                 print('no solutions from', jFirst_site, 'to', jSecond_site, 'at time', tmp_step_starting_time)
                break
            #             tmp_current_from_to_ddf['delay'] =
            #             print(tmp_current_from_to_ddf['Date'])
            #             tmp_current_from_to_ddf['Date'] - starting_time
            time_delta_se = tmp_current_from_to_ddf['Date'] - tmp_step_starting_time
            closest_time_index = time_delta_se.idxmin()
            tmp_step_time_duration = tmp_current_from_to_ddf.loc[closest_time_index, 'Duration'].astype(float)

            #             tmp_step_time_duration = ddf.query(
            # #                 'interval_start >= @tmp_step_starting_time and interval_end >= @tmp_step_ending_time and from == @jFirst_site and to == second == @jSecond_site'
            #                 'interval_start >= @tmp_step_starting_time and interval_end >= @tmp_step_ending_time and from == @jFirst_site and to == second == @jSecond_site'
            #             )['duration'].values
            if tmp_step_time_duration < 0:  # no connection
                break
            tmp_step_time_duration += site2duration[jSecond_site]
            # Otherwise we could directly put the time
            tmp_step_starting_time += datetime.timedelta(seconds=tmp_step_time_duration)
            #             tmp_step2dep_time[
            #                 (tmp_current_from_to_ddf.loc[closest_time_index, 'Origin'],
            #                  tmp_current_from_to_ddf.loc[closest_time_index, 'Destination']
            #                 )
            #             ] = tmp_current_from_to_ddf.loc[closest_time_index, 'Date']
            tmp_step_time_ls += [
                {'from': tmp_current_from_to_ddf.loc[closest_time_index, 'Origin'],
                 'to': tmp_current_from_to_ddf.loc[closest_time_index, 'Destination'],
                 'time': tmp_current_from_to_ddf.loc[closest_time_index, 'Date'].strftime('%Y-%m-%dT%H:%M:%S')
                 }
            ]
            # tmp_itinerary_time_duration += tmp_step_time_duration

        if tmp_step_time_duration > 0:
            tmp_itinerary_time_duration = pd.Timedelta(tmp_step_starting_time - starting_time).seconds
            path2time_duration[iItinerary_tuple] = tmp_itinerary_time_duration
            path2end_time[iItinerary_tuple] = tmp_step_starting_time
            path2step2dep_time[iItinerary_tuple] = tmp_step_time_ls

    return path2time_duration, path2end_time, path2step2dep_time


def get_best_solution(starting_time, sites_to_visit_ls):
    ddf = pd.read_csv('durations.csv')
    ddf['Date'] = pd.to_datetime(ddf['Date'])
    path2time_duration, path2end_time, path2step2dep_time = compute_all_itineraries_duration(
        ddf, site2duration, starting_location,
        starting_time, sites_to_visit_ls
    )
    best_solution = min(path2time_duration, key=path2time_duration.get)
    loc_list = path2step2dep_time[best_solution]

    return path2time_duration, loc_list, path2end_time[best_solution]



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
