from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
import json
from bson import json_util
from bson.json_util import dumps
import operator
# import yaml
import urllib
from datetime import datetime
import requests

app = Flask('fyl_Umich')
mongo = PyMongo(app)


# # function for return data for making dropdown
def all_leader_name_id():

	collection_leader = mongo.db.leaders
	dic={}
	dic_save=[]

	for a in collection_leader.distinct('chamber'):
		for b in collection_leader.distinct('party'):
			pass
			#dic.setdefault([a,b],[])
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
	r = requests.get(a['photo_url'])
	if r.status_code == 404:

		a['photo_url']=a['photo_url'].replace(".JPG", "_400x400.JPG");
		a['photo_url']=a['photo_url'].replace(".jpg", "_400x400.jpg");
		a['photo_url']=a['photo_url'].replace(".jpeg", "_400x400.jpeg");
		
		g = requests.get(a['photo_url']) 
		if g.status_code == 404:
			a['photo_url']="https://avatars.io/twitter/"+a['twitter_name']


	return a


# function for loading the time series data (#Tweets)
def load_timeserie_fuc(user0="H001061"):


	timeline=mongo.db.timelines.find_one({"bioguide":user0}, {'_id': False})
	return timeline if timeline != None else {}
# function for load data for hashtage
def load_hash_data(user0="H001061"):

	#https://stackoverflow.com/questions/12345387/removing-id-element-from-pymongo-results
	#print mongo.db.urls.find_one({"bioguide":user0}, {'_id': False})
	hashdata= mongo.db.hashtages.find_one({"bioguide":user0}, {'_id': 0})

	return hashdata if hashdata != None else {}


# function for loading data for urls
def load_url_data(user0="H001061"):

	urls=mongo.db.urls.find_one({"bioguide":user0}, {'_id': 0})

	return urls if urls != None else {}



