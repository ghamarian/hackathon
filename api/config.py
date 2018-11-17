import pandas as pd

locations = {
    "centraal": [52.080395, 4.325370],
    "maduradam": [52.0995, 4.2969],
    "gemeentemuseume": [52.0899, 4.2807],
    "kijkduin": [52.0614, 4.2218],
    "de uithof": [52.0382, 4.2416],
    "haagsemarkt": [52.0646, 4.2991],
    "mauritshuis": [52.0804, 4.3143],
    "familiepark drievliet": [52.0551, 4.3499],
    "huistenbosch": [52.093256, 4.343400],
    "Museum Voorlinden": [52.1185, 4.3459],
    "scheveningen": [52.1145, 4.2790]
}

URL = "https://api-acc.anwb.nl/v1/routing"
APIKEY = "bjUtF51yGCVatPljvWNcYpv9MQE7efLj"
LANG = 'en-GB'

HEADERS = {
    'Content-Type': "application/x-www-form-urlencoded",
    'x-anwb-client-id': "{{anwb_client_id}}",
    'Authorization': "Bearer {{token}}",
    'cache-control': "no-cache",
    'Postman-Token': "49e44fdb-1247-4ca9-84ad-372ef2ee6c03"
}

OPTIONS = {
    "transportMode": {"car", "bike", "pedestrian", "publicTransport"},
    "language": {"en-Gb", "nl-Nl"},
    "dateTime": "YYYY-MM-DDTHH:mm:ss",
    "timeType": {"depart", "arrival"},
    "instructions": {"true", "false"},
    "locations": "l,l:l,l",
    "maxAlternatives": 0,
    "routeType": {"fastest", "shortest", "eco", "thrilling"},
    "avoidPublicTransportTypes": {"tram", "train", "ferry", "metro", "bus"},
    "avoid": {"tollRoads", "motorways", "ferries", "unpavedRoads", "allreadyUsedRoads", "obstructions"},
    "polyline": {"true", "false"}
}

all_site_ls = [
    'Den Haag Centraal',
    'Maduroam',
    'Gemeentemuseum Den Haag',
    'Kijkduin',
    'De Uithof',
    'Haagse Markt',
    'Mauritshuis',
    'Familiepark Drievliet',
    'Huis Ten Bosch',
    'Museum Voorlinden',
    'Scheveningen'
]

locations_map = [
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

mapping = {locations_map[i]: all_site_ls[i] for i in range(len(locations_map))}

print(mapping)
