import json

def parseGeoLocationJSON(_info) :
    json_info = _info
    status = json_info["status"]
    latitude = json_info["results"][0]["geometry"]["location"]["lat"]
    longitude = json_info["results"][0]["geometry"]["location"]["lng"]
    place_id = json_info["results"][0]["place_id"]

    return status, latitude, longitude, place_id