#!/usr/bin/env python

from configparser import ConfigParser
import requests
import random
from pprint import pprint

config = ConfigParser()
config.readfp(open('.cfg'))
lat = config.get('all','lat')
lon = config.get('all','lon')
zomato_api_key = config.get('all','zomato_api_key')
radius_metres = config.get('all','radius_metres')

header = {"User-agent": "curl/7.43.0", 
          "Accept": "application/json", 
          "user_key": zomato_api_key  }

cuisines_url = 'https://developers.zomato.com/api/v2.1/cuisines?lat={lat}&lon={lon}'.format(lat=lat, lon=lon)
cuisines_json = requests.get(cuisines_url,headers=header).json()

cuisines = cuisines_json['cuisines']

random_cuisine = random.choice(cuisines)


cuisine_id = random_cuisine['cuisine']['cuisine_id']
cuisine_name = random_cuisine['cuisine']['cuisine_name']

print()
print('Randomly chose:', cuisine_name)

sort = 'rating'
order = 'desc'
category_dinner = 10

restaurant_search_url = 'https://developers.zomato.com/api/v2.1/search?lat={lat}&lon={lon}&radius={radius}&cuisines={cuisine_id}&category={category}&sort={sort}&order={order}'.format(lat=lat,lon=lon,radius=radius_metres,cuisine_id=cuisine_id,sort=sort,order=order,category=category_dinner)

restaurants_json = requests.get(restaurant_search_url, headers=header).json()

restaurant_names = [(x['restaurant']['name'],x['restaurant']['url'],x['restaurant']['average_cost_for_two']) for x in restaurants_json['restaurants']]

km = int(radius_metres)/1000.

print("--------------------")
print("Highest rated restaurants within {km} km from home:".format(km=km))
print()

if len(restaurant_names) == 0:
	print("Nothing found matching search criteria :(")
	print()
	exit()

for name, url, avg_cost in restaurant_names:
	url = url.split('?')[0]
	print(name, url, '~$', avg_cost, 'for two people')
#pprint(restaurants_json)
print()
print("Enjoy date night!")
print()
