from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file, Response
import polyline as pll
import os

from api import routing, config
import json

app = Flask(__name__)
Bootstrap(app)

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyC7Ba8Iu-wTrwTwgc4FZdGFwMmZkjbCUuk"

# Initialize the extension
GoogleMaps(app)

# app = Flask(__name__, template_folder=".")
# GoogleMaps(app)

venues = []

poly_coords = [
    (52.1145, 4.2790),
    (52.0995, 4.2969),
    (52.0899, 4.2807),
    (52.0614, 4.2218),
    (52.0382, 4.2416),
    (52.0646, 4.2991),
    (52.0804, 4.3143),
    (52.0551, 4.3499),
    (52.0930, 4.3438),
    (52.1185, 4.3459)
]


# I am posting here the URL of the 10 destinations:
# Scheveningen :: https://media-cdn.tripadvisor.com/media/photo-s/01/37/7c/ab/scheveningen.jpg
# Madurodam :: https://tickets.holland.com/wp-content/uploads/2016/09/madurodam.jpg
# Gemeentemuseum Den Haag :: https://www.gemeentemuseum.nl/sites/default/files/styles/full_width_768x2/public/images/Museum/Ons%20verhaal/Gebouw/Foto%27s%20gebouw/centrale%20hal%20DEF.jpg
# Kijkduin :: https://upload.wikimedia.org/wikipedia/commons/b/b6/2008-Kijkduin-Strandpromenade-1.jpg
# De Uithof :: https://cdn.wintersport.nl/destinations/3/42749.jpg?w=1280
# Haagse Markt :: https://dehaagsemarkt.nl/wp-content/uploads/2016/08/Haagse-Markt-9283.jpg
# Mauritshuis :: https://www.holland.com/upload_mm/f/b/5/64127_fullimage_hofvijver_ivo_hoekstra.jpg
# Familiepark Drievliet :: https://findapinball.com/media/foursquare/familiepark-drievliet_51f272a8498e44d4ebecb821.jpg
# Huis Ten Bosch :: https://www.tracesofwar.com/upload/2589180707235002.jpg
# Museum Voorlinden ::  http://www.kraaijvanger.nl/image/1/0/1080/0/uploads/project-afbeeldingen/3065_02_n195_medium-57c84ff9a0c71.jpg

destinations = [{'name': 'scheveningen',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.1145,
                 'lng': 4.279,
                 'infobox': '<b>$scheveningen</b>',
                  'img': 'https://media-cdn.tripadvisor.com/media/photo-s/01/37/7c/ab/scheveningen.jpg'},
                {'name': 'maduradam',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.0995,
                 'lng': 4.2969,
                 'infobox': '<b>$maduradam</b>',
                 'img': 'https://tickets.holland.com/wp-content/uploads/2016/09/madurodam.jpg'

                 },
                {'name': 'gemeentemuseume',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.0899,
                 'lng': 4.2807,
                 'infobox': '<b>$gemeentemuseume</b>',
                 'img': 'https://www.gemeentemuseum.nl/sites/default/files/styles/full_width_768x2/public/images/Museum/Ons%20verhaal/Gebouw/Foto%27s%20gebouw/centrale%20hal%20DEF.jpg'
                 },
                {'name': 'kijkduin',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.0614,
                 'lng': 4.2218,
                 'infobox': '<b>$kijkduin</b>',
                 'img': 'https://upload.wikimedia.org/wikipedia/commons/b/b6/2008-Kijkduin-Strandpromenade-1.jpg',
                 },
                {'name': 'de uithof',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.0382,
                 'lng': 4.2416,
                 'infobox': '<b>$de uithof</b>',
                 'img': 'https://cdn.wintersport.nl/destinations/3/42749.jpg?w=1280'
                 },
                {'name': 'haagsemarkt',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.0646,
                 'lng': 4.2991,
                 'infobox': '<b>$haagsemarkt</b>'},
                {'name': 'mauritshuis',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.0804,
                 'lng': 4.3143,
                 'infobox': '<b>$mauritshuis</b>',
                 'img': 'https://www.holland.com/upload_mm/f/b/5/64127_fullimage_hofvijver_ivo_hoekstra.jpg'},
                {'name': 'familiepark drievliet',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.0551,
                 'lng': 4.3499,
                 'infobox': '<b>$familiepark drievliet</b>',
                 'img': 'https://findapinball.com/media/foursquare/familiepark-drievliet_51f272a8498e44d4ebecb821.jpg'},
                {'name': 'huistenbosch',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.0930,
                 'lng': 4.3438,
                 'infobox': '<b>$huistenbosch</b>',
                 'img': 'https://www.tracesofwar.com/upload/2589180707235002.jpg'},
                {'name': 'Museum Voolinden',
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 52.1185,
                 'lng': 4.3459,
                 'infobox': '<b>$Museum Voorlinden</b>',
                 'img': 'http://www.kraaijvanger.nl/image/1/0/1080/0/uploads/project-afbeeldingen/3065_02_n195_medium-57c84ff9a0c71.jpg'}]

polyline = {
    'stroke_color': '#0AB0DE',
    'stroke_opacity': 1.0,
    'stroke_weight': 3,
    # 'path':  [(52.1145,4.2790)],
}

polylines = [polyline] + [poly_coords]

sndmap = Map(
    identifier="thirdmap",
    lat=52.1145,
    lng=4.2790,
    markers=destinations,
    polylines=polylines,
    zoom=12,
    style="height:800px;width:800px;margin:0;",

)


def draw_map(locA, locB, date):
    summary, route = routing.query(date, config.locations[locA], config.locations[locB])
    poly_line = route[0]['polyline']
    poly_coords = pll.decode(poly_line)
    stops = route[0]['instructions']
    destinations = []

    for x in stops:
        dep = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            'lat': x['departure']['point']['lat'],
            'lng': x['departure']['point']['lon'],
        }
        if 'stop' in x['departure']:
            dep['infobox'] = '<b>' + x['departure']['city'] + ' - ' + x['departure']['stop'] + '</b>'

        destinations.append(dep)
        arr = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            'lat': x['arrival']['point']['lat'],
            'lng': x['arrival']['point']['lon']}
        if 'stop' in x['arrival']:
            arr['infobox'] = '<b>' + x['arrival']['city'] + ' - ' + x['arrival']['stop'] + '</b>'

        destinations.append(arr)

    destinations.append({
        'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
        'lat': destinations[0]['lat'],
        'lng': destinations[0]['lng'],
        'infobox': '<b>' + config.mapping[locA] + '</b>'

    })
    destinations.append({
        'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
        'lat': destinations[-2]['lat'],
        'lng': destinations[-2]['lng'],
        'infobox': '<b>' + config.mapping[locB] + '</b>'

    })
    destinations = [destinations[-1], destinations[-2]]
    return destinations, poly_coords


def multiple_routes(loc_list):
    lat = config.locations[loc_list[0]['from']][0]
    lng = config.locations[loc_list[0]['from']][1]
    destinations = []
    poly_coords = []
    for i in range(len(loc_list)):
        locA = loc_list[i]['from']
        locB = loc_list[i]['to']
        date = loc_list[i]['time']
        d, p = draw_map(locA, locB, date)
        destinations += d
        poly_coords += p
    # destinations = [item for sublist in destinations for item in sublist]
    # poly_coords = [item for sublist in poly_coords for item in sublist]

    sndmap = Map(
        identifier="map",
        lat=lat,
        lng=lng,
        markers=destinations,
        polylines=[poly_coords],
        zoom=12,
        style="height:800px;width:800px;margin:0;",

    )
    return sndmap


@app.route("/show_map")
def venues():
    startingtime = '2018-11-17T10:20:00'
    places_to_visit = ['mauritshuis', 'kijkduin', 'maduradam']
    time, loc_list, _ = routing.get_best_solution(startingtime, places_to_visit)

    sndmap = multiple_routes(loc_list)
    return render_template('show_map.html', sndmap=sndmap)

@app.route("/")
def index():
    # mymap = Map(
    #     identifier="view-side",
    #     lat=37.4419,
    #     lng=-122.1419,
    #     markers=[(37.4419, -122.1419)]
    # )
    return render_template('venues.html', destinations=destinations)


# @app.route('/venues', methods=['GET', 'POST'])
# def all():
#
#     venues = json.loads(request.form['venues'])
#     names = [destinations[i] for i in venues]
#
#     return render_template('show_map.html', sndmap=sndmap)

if __name__ == "__main__":
    os.environ['FLASK_DEBUG'] = '1'
    app.run(debug=True)
