import json
import urllib.request
import requests
from pprint import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "O1gGM8CKRPGplNw9tGa0zLl1GZUIYdsc"
MBTA_API_KEY = "3bc6e803e2a346e4bf0a815e4be453d2"

def get_json(url):
    response = requests.request("GET", url)
    response_data = (response.json())
    return response_data


def get_lat_long(place_name):
    place = place_name+', MA' #I added this to force the API to search only in Massachusetts
    
    url = f'{MAPQUEST_BASE_URL}?key={MAPQUEST_API_KEY}&location={place}'
    place_json = get_json(url)
    pprint(place_json)
    print(len(place_json["results"][0]["locations"])) 
    latlon = []
    for i in range(0, len(place_json["results"][0]["locations"])):
        country = place_json["results"][0]["locations"][i]["adminArea1"]
        state = place_json["results"][0]["locations"][i]["adminArea3"]
        if(country == "US" and state=="MA"):
            #pprint(place_json["results"][0]["locations"][i])
            temp = []
            lat = place_json["results"][0]["locations"][i]["latLng"]["lat"] # modify this so you get the correct latitude
            lon = place_json["results"][0]["locations"][i]["latLng"]["lng"] # modify this so you get the correct longitude
            temp.append(lat)
            temp.append(lon)
            latlon.append(temp)
    #pprint(latlon)
    return latlon


def get_nearest_station(pairs):
    #print(len(pairs))
    nearest_station = {}
    for i in range(0, len(pairs)):
        latitude = pairs[i][0]
        longitude = pairs[i][1]

        url = f'{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&fields%5Bstop%5D=name,description,latitude,longitude,wheelchair_boarding&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance&radius=0.05'
        station_json = get_json(url)

        wheelchair_boarding = []

        print("List of all stations sorted by distance:")
        for w in range(0, len(station_json["data"])):
            wheelboarding = (station_json["data"][w]["attributes"]["wheelchair_boarding"])
            desc = (station_json["data"][w].get("attributes")["description"])
            name = (station_json["data"][w].get("attributes")["name"])
            counter = w+1

            if (wheelboarding == 1):
                if(str(desc) == "None"):
                    station = str(name) + ": This station is wheelchair accessible"
                    nearest_station[counter] = station
                else:
                    station = str(desc) + ": This station is wheelchair accessible"
                    nearest_station[counter] = station
            else:
                if(str(desc) == "None"):
                    station = str(name) + ": This station is wheelchair accessible"
                    nearest_station[counter] = station
                else:
                    station = str(desc) + ": This station is not wheelchair accessible"
                    nearest_station[counter] = station
        return nearest_station


def find_stop_near(place_name):
    return get_nearest_station(*get_lat_long(place_name))


def answer(location):
    #places = input('Enter a place name in Boston such as "Fenway Park": ')
    lat_lon_pairs = get_lat_long(location)

    return(get_nearest_station(lat_lon_pairs)) 
