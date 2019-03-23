#!/usr/bin/env python

from configparser import ConfigParser
import requests
import random
from pprint import pprint
from tabulate import tabulate
#from collections import namedtuple

#Restaurant = namedtuple('Restaurant', 'name url average_cost_for_two rating votes locality')

# get settings from .cfg
config = ConfigParser()
config.read_file(open('.cfg'))
lat = config.get('all', 'lat')  # location
lon = config.get('all', 'lon')
zomato_api_key = config.get('all', 'zomato_api_key')  # api key
radius_metres = config.get('all', 'radius_metres')  # search radius
sort_by = config.get('all', 'sort_by')
sort_direction = config.get('all', 'sort_direction')

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

sort = sort_by
order = sort_direction
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

results = [['Name', 'URL', 'Average cost for two ($)', 'Rating', 'Votes', 'Locality']]
for x in restaurants_json['restaurants']:
    results.append(
        [
            x['restaurant']['name'],
            x['restaurant']['url'].split('?')[0], # remove the extra url cruft
            x['restaurant']['average_cost_for_two'],
            x['restaurant']['user_rating']['aggregate_rating'],
            x['restaurant']['user_rating']['votes'],
            x['restaurant']['location']['locality']
        ]
    )

# convert to km for human readability
km = int(radius_metres)/1000.

print(f"Restaurant search for location ({lat}, {lon}) radius {km} km sorted {sort_by}, {sort_direction}:")

if len(results) == 1:  # only table headings
    print("Nothing found matching search criteria :(\n")
else:
    print(tabulate(results))
    print("\nEnjoy date night!\n")