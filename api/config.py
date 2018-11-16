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
