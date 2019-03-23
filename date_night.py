#!/usr/bin/env python

from configparser import ConfigParser
import requests
import random
from pprint import pprint

# get settings from .cfg
config = ConfigParser()
config.read_file(open('.cfg'))
lat = config.get('all', 'lat')  # location
lon = config.get('all', 'lon')
zomato_api_key = config.get('all', 'zomato_api_key')  # api key
radius_metres = config.get('all', 'radius_metres')  # search radius

# set API call header
header = {
    "User-agent": "curl/7.43.0",
    "Accept": "application/json",
    "user_key": zomato_api_key
}

# set up API call params
payload = {
    'lat': lat,
    'lon': lon
}

# get list of cuisines available at location
cuisines_url = 'https://developers.zomato.com/api/v2.1/cuisines'
cuisines_json = requests.get(
    cuisines_url,
    params=payload,
    headers=header).json()
cuisines = cuisines_json['cuisines']

random_cuisine = random.choice(cuisines)

cuisine_id = random_cuisine['cuisine']['cuisine_id']
cuisine_name = random_cuisine['cuisine']['cuisine_name']

print('\nWhich cuisine reins supreme?\n')
print('Randomly chose cuisine:', cuisine_name)

sort = 'rating'
order = 'desc'
category_dinner = 10

restaurant_search_url = 'https://developers.zomato.com/api/v2.1/search'
payload = {
    'lat': lat,
    'lon': lon,
    'radius': radius_metres,
    'cuisines': cuisine_id,
    'sort': sort,
    'order': order,
    'category': category_dinner,
}

restaurants_json = requests.get(restaurant_search_url, params=payload, headers=header).json()

restaurant_names = [
    (
        x['restaurant']['name'],
        x['restaurant']['url'],
        x['restaurant']['average_cost_for_two']
    )
    for x in restaurants_json['restaurants']
]

# convert to km for human readability
km = int(radius_metres)/1000.

print("-" * 20)
print(f"Highest rated restaurants within {km} km from home:\n")

# if no restaurants found for cuisine, location, radius print sad message
if len(restaurant_names) == 0:
    print("Nothing found matching search criteria :(\n")
    exit()

# for each suggested restaurant, print its name, url and average cost for two people
for name, url, avg_cost in restaurant_names:
    url = url.split('?')[0]  # remove the extra url cruft
    print(name, url, '~$', avg_cost, 'for two people')

print("\nEnjoy date night!\n")
