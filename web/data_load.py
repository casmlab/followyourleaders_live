from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
import json
from bson import json_util
from bson.json_util import dumps
import operator
import urllib
from datetime import datetime
import requests
import os

app = Flask(__name__)
if 'FYL_CONFIG' in os.environ:
    app.config.from_envvar('FYL_CONFIG')
else:
    app.config.from_object('config')

mongo = PyMongo(app)

# # function for preparing data for making drop downs
def all_leader_name_id():

	collection_leader, dic, dic_save = mongo.db.leaders, {}, []

	for a in collection_leader.distinct('chamber'):
		for b in collection_leader.distinct('party'):
			pass
			dic.setdefault((a,b),[])

	for leader in collection_leader.find():
		dic[(leader['chamber'],leader['party'])].append({"bioguide": leader['bioguide'], "name": leader['name']})

	for key,value in dic.items():
		temp={}
		temp['chamber_car']=key[0]
		temp['party_cat']=key[1]
		temp['leader']=value
		dic_save.append(temp)

	return dic_save


# # function for loading the basic information of leader
def load_basic_info_fuc(user0="H001061"):

	#check if the url of photo is 404
	a = mongo.db.leaders.find_one({'bioguide': user0}, {'_id': 0})
	if a:
		r = requests.get(a['photo_url'])
		if r.status_code == 404:
			a['photo_url']=a['photo_url'].replace(".JPG", "_400x400.JPG");
			a['photo_url']=a['photo_url'].replace(".jpg", "_400x400.jpg");
			a['photo_url']=a['photo_url'].replace(".jpeg", "_400x400.jpeg");
			g = requests.get(a['photo_url']) 
			if g.status_code == 404:
				a['photo_url']="https://avatars.io/twitter/"+a['twitter_name']

		if "chamber" in  a:
			a['chamber_name'] = 'Senate' if a["chamber"]=='sen' else 'House'

	return a


# function for loading time series data (#Tweets)
def load_timeserie_fuc(user0="H001061"):
	timeline=mongo.db.timelines.find_one({"bioguide":user0}, {'_id': False})
	return timeline if timeline != None else {}

# function for loading urls data
def load_url_data(user0="H001061"):
	urls=mongo.db.urls.find_one({"bioguide":user0}, {'_id': 0})
	return urls if urls != None else {}

# function for loading hashtags data
def load_hash_data(user0="H001061"):
	hashdata= mongo.db.hashtags.find_one({"bioguide":user0}, {'_id': 0})
	return hashdata if hashdata != None else {}



