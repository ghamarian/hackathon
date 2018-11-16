from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyC7Ba8Iu-wTrwTwgc4FZdGFwMmZkjbCUuk"

# Initialize the extension
GoogleMaps(app)


# app = Flask(__name__, template_folder=".")
# GoogleMaps(app)

@app.route("/")
def mapview():

    # mymap = Map(
    #     identifier="view-side",
    #     lat=37.4419,
    #     lng=-122.1419,
    #     markers=[(37.4419, -122.1419)]
    # )

    poly_coords = [
        (52.1145,4.2790),
        (52.0995,4.2969 ),
        (52.0899,4.2807),
        (52.0614,4.2218),
        (52.0382,4.2416),
        (52.0646,4.2991),
        (52.0804,4.3143),
        (52.0551,4.3499),
        (52.0930, 4.3438),
        (52.1185,4.3459)
    ]

    destinations = [{'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.1145,
      'lng': 4.279,
      'infobox': '<b>$scheveningen</b>'},
     {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.0995,
      'lng': 4.2969,
      'infobox': '<b>$maduradam</b>'},
     {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.0899,
      'lng': 4.2807,
      'infobox': '<b>$gemeentemuseume</b>'},
     {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.0614,
      'lng': 4.2218,
      'infobox': '<b>$kijkduin</b>'},
     {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.0382,
      'lng': 4.2416,
      'infobox': '<b>$de uithof</b>'},
     {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.0646,
      'lng': 4.2991,
      'infobox': '<b>$haagsemarkt</b>'},
     {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.0804,
      'lng': 4.3143,
      'infobox': '<b>$mauritshuis</b>'},
     {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.0551,
      'lng': 4.3499,
      'infobox': '<b>$familiepark drievliet</b>'},
     {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.0930,
      'lng': 4.3438,
      'infobox': '<b>$huistenbosch</b>'},
     {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      'lat': 52.1185,
      'lng': 4.3459,
      'infobox': '<b>$Museum Voorlinden</b>'}]

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
    return render_template('map.html', sndmap=sndmap)

if __name__ == "__main__":
    app.run(debug=True)
