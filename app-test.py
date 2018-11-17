from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyC7Ba8Iu-wTrwTwgc4FZdGFwMmZkjbCUuk"

# Initialize the extension
GoogleMaps(app)


# app = Flask(__name__, template_folder=".")
# GoogleMaps(app)

polyline = {
    'stroke_color': '#0AB0DE',
    'stroke_opacity': 1.0,
    'stroke_weight': 3,
    'path': [{'lat': 33.678, 'lng': -116.243},
             {'lat': 33.679, 'lng': -116.244},
             {'lat': 33.680, 'lng': -116.250},
             {'lat': 33.681, 'lng': -116.239},
             {'lat': 33.678, 'lng': -116.243}]
}

path1 = [(33.665, -116.235), (33.666, -116.256),
         (33.667, -116.250), (33.668, -116.229)]

path2 = ((33.659, -116.243), (33.660, -116.244),
         (33.649, -116.250), (33.644, -116.239))

path3 = ([33.688, -116.243], [33.680, -116.244],
         [33.682, -116.250], [33.690, -116.239])

path4 = [[33.690, -116.243], [33.691, -116.244],
         [33.692, -116.250], [33.693, -116.239]]

polylines = [polyline, path1, path2, path3, path4]

@app.route("/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=33.4419,
        lng=-116.1419,
        markers=[(33.4419, -116.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=33.4419,
        lng=-116.1419,
        zoom=10,
        style="height:800px;width:800px;margin:0;",
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 33.4419,
             'lng': -116.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 33.4300,
             'lng': -116.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ],
        polylines=polylines
    )
    return render_template('venues.html', mymap=mymap, sndmap=sndmap)

if __name__ == "__main__":
    app.run(debug=True)
