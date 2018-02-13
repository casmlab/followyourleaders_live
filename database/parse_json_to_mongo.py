__author__ = "Pai-ju Chang, Libby Hemphill"
__maintainer__ = "Pai-ju Chang"
__email__ = "paiju@umich.edu"
__status__ = "Development"

# Something here about what the code does

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pymongo/__init__.py')

from pymongo import MongoClient
import pymongo
from bson import json_util
from bson.json_util import dumps
import json
import numpy as np
import pickle
import time
import urllib
import yaml
from collections import defaultdict
import itertools
import requests


# define class
class followyourleaders(object):
	def __init__(self):
		self.a = 1


	############################# for creating yaml collection (will be dropped after the leader collection is built) #############################
	# def create_yaml_collection(self):
	# 	# reset yaml collection
	# 	print('>>> create_yaml_collection() starts!')
	# 	collection_yaml.drop()

	# 	# read yaml files
	# 	print('>>> reading yaml files')
	# 	legislators_file = urllib.request.urlopen('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml')
	# 	lst_a = yaml.load(legislators_file)
	# 	media = urllib.request.urlopen('https://theunitedstates.io/congress-legislators/legislators-social-media.yaml')
	# 	lst_b = yaml.load(media)


	# 	# merge yaml files
	# 	lst = sorted(itertools.chain(lst_b,lst_a), key=lambda x:x['id']['bioguide'])
	# 	lst_legislators = []
	# 	for k,v in itertools.groupby(lst, key=lambda x:x['id']['bioguide']):
	# 	    d = {}
	# 	    for dct in v:
	# 	        d.update(dct)
	# 	    lst_legislators.append(d)


	# 	# insert into database
	# 	for dct in lst_legislators:
	# 		collection_yaml.insert(dct)
	# 	print('>>> create_yaml_collection() ends!')


	# ############################# for creating leader collection and dropping yaml collection (source: yaml collection)#############################
	# ############################# this leader collection is not completed, the recent tweets, followers, friends and description need ###############
	# ############################# to be updated by update_recent_info_by_tweets function ###########################################################
	# def create_leaders_collection (self) :
	# 	print('>>> create_leaders_collection() starts!')

	# 	# read from yamls collection
	# 	yamls = collection_yaml.find()
	# 	collection_leader.drop()


	# 	for yaml in yamls:
	# 		# if this leader has used social media
	# 		if 'social' in yaml:
	# 			# if this leader has used twitter
	# 			if 'twitter' in yaml['social']:
	# 				# if this leader is in yamls.
	# 				if 'bio' in yaml:

	# 					if 'religion' in yaml['bio']:
	# 						religion = yaml['bio']['religion']
	# 					else:
	# 						religion = 'Unknown'
	# 					state = yaml['terms'][0]['state']
	# 					chamber =  yaml['terms'][0]['type']
	# 					party = yaml['terms'][0]['party']
	# 					if 'twitter_id' in yaml['social']:
	# 						twitter_id = str(yaml['social']['twitter_id'])
	# 					else:
	# 						twitter_id = 'NA'

	# 					photo_url = requests.get('https://twitter.com/'+yaml['social']['twitter']+'/profile_image?size=original').url

	# 					# form data structure by datamodel.md
	# 					leader_dict = {'twitter_name':yaml['social']['twitter'],'bioguide':yaml['id']['bioguide'],'twitter_id':twitter_id
	# 					,'name':yaml['name']['official_full'],'gender':yaml['bio']['gender'],'birthday':yaml['bio']['birthday'],
	# 					 'religion':religion,'state':state,'chamber':chamber,'party':party,'wikidata':yaml['id']['wikidata'],"photo_url":photo_url}

	# 					# insert into database
	# 					collection_leader.insert(leader_dict)


	# 	# drop  yaml collection
	# 	# collection_yaml.drop()
	# 	print('>>> create_leaders_collection() ends!')


	############################# for creating timelines (source: tweets collection) #########################

	# def create_timeline_collection(self, tweets):

	# 	print('>>> create_timeline_collection(self, tweets) starts!')
	# 	collection_timeline.drop()

	# 	for tweet in tweets:

	# 		leader = collection_leader.find_one({"twitter_id" : tweet['user']['id_str']})

	# 		# check is or isnt this user a the leader
	# 		if leader != None:

	# 			# define date/time formats
	# 			post_date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
	# 			post_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

	# 			# create/update timelines collection
	# 			leader_timeline = collection_timeline.find_one({"bioguide" : leader['bioguide']})

	# 			# define update location
	# 			keyidx = "dates."+post_date+"."+tweet['id_str']

	# 			# define inserting/updating item format
	# 			url = 'https://twitter.com/'+tweet['user']['screen_name']+'/status/'+tweet['id_str']
	# 			item_push = {'hashtags': [a['text'] for a in tweet['entities']['hashtags']],'created_at':post_date_time,
	# 			'url':url}

	# 			# if we dont have the leader's information in timeline collection, insert one for him/her
	# 			if  leader_timeline == None:

	# 				print('start inserting '+leader['bioguide'] +' into timelines collection')
	# 				dic={}
	# 				dic['twitter_name']=tweet['user']['screen_name']
	# 				dic['twitter_id']=tweet['user']['id_str']
	# 				dic['bioguide']=leader['bioguide']
	# 				dic.setdefault('dates', {})
	# 				collection_timeline.insert(dic)


	# 			# update timeline collection from tweets
	# 			collection_timeline.update( { 'bioguide': leader['bioguide']},{ '$set': { keyidx: item_push } } )


	# 	print('>>> create_timeline_collection(self, tweets) ends!')

	#############################  function for creating hashtags collections  #########################

	def create_hashtag_collection(self, tweets):

		print('>>> create_hashtags_collection(self, tweets) starts!')
		collection_hashtags.drop()

		for tweet in tweets:

			leader = collection_leader.find_one({"twitter_id" : tweet['user']['id_str']})

			# check is or isnt this user a the leader
			if leader != None:

				# define date/time formats
				post_date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				post_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

				leader_hashtags = collection_hashtags.find_one({"bioguide" : leader['bioguide']})
				
				# check if the leader is already in hashtags collection, if not, insert information for them to collection
				if leader_hashtags == None:

					print('start inserting ' + leader + ' into hashtags collection')
					dic = {}
					dic['bioguide'] = leader
					dic.setdefault('hashtags', {})
					collection_hashtags.insert(dic)


				# update hashtags collection from tweets
				for a in tweet['entities']['hashtags']:
					key_idx = "hashtags." + a['text'] + ".tweets." + tweet['id_str']
					collection_hashtags.update({ 'bioguide': leader }, { '$set': {key_idx+'.text':tweet['text'],key_idx + '.created_at':post_date_time} } )
					

		print('>>> create_hashtags_collection(self, tweets) ends!')


		#############################  function for creating/updaing urls collections#########################
		# def create_url_collection (self,tweets):

		# 	print('>>> create_url_collection(self, tweets) starts!')
		# 	collection_url.drop()

		# 	for tweet in tweets:

		# 		leader = collection_leader.find_one({"twitter_id" : tweet['user']['id_str']})

		# 		# check is or isnt this user a the leader
		# 		if leader != None:

		# 			# define date/time formats
		# 			post_date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
		# 			post_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

		# 			# read leader's information from urls collection
		# 			leader_url = collection_url.find_one({"bioguide" : leader})
		

		# 			# if we dont have the leader's information in urls collection, insert one for him/her
		# 			if leader_url == None:

		# 				print('start inserting '+ leader +' into urls collection')
		# 				dic = {}
		# 				dic['bioguide'] = leader
		# 				dic.setdefault('urls', {})
		# 				collection_url.insert(dic)


		# 			#update urls collection from tweets
		# 			for a in tweet['entities']['urls']:
		# 				#keyinde="urls."+a['url'].replace('.', '\u002e')+".tweets."+tweet['id_str']
		# 				# print(a['url'].split("t.co/"))
		# 				key_idx = "urls." + a['url'].split("t.co/")[1] + ".tweets." + tweet['id_str']
		# 				collection_url.update( { 'bioguide': leader },{ '$set': {key_idx + '.text':tweet['text'], key_idx + '.created_at':post_date_time} } )

		# 	print('>>> create_url_collection(self, tweets) ends!')


	# #############for updating "recent_tweets", "followers", "friends", "description" in leader collection (by timeline, tweets, leaders collections)#############################
	# def update_recent_info_by_tweets(self,show_number):
	# 	print('>>> update_recent_info_by_tweets(show_number) starts!')
    #
	# 	# load data from leader collection
	# 	leaders = collection_leader.find()
    #
	# 	for leader in leaders:
    #
	# 		show_number_item = show_number
	# 		date_index = []
	# 		text_index = []
    #
	# 		# check whether we have his/her Twitter data
	# 		item = collection_timeline.find_one({"bioguide" : leader['bioguide']})
    #
    #
    #
	# 		# if we have this leader's data
	# 		if item != None:
    #
	# 			a = item['dates'].keys()
    #
	# 			# sort by time https://stackoverflow.com/questions/5166842/sort-dates-in-python-array
	# 			a.sort(key = lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")),reverse=True)
	# 			#print(a)
    #
	# 			for u in a:
    #
	# 				sublist = item['dates'][u]
	# 				temp = [(key,value['created_at']) for key,value in sublist.items()]
    #
	# 				temp.sort(key = lambda x: time.mktime(time.strptime(x[1],"%Y-%m-%d %H:%M:%S")),reverse=True)
    #
	# 				# decide #twitter we need to insert
	# 				admin = min(len(sublist),show_number_item)
	# 				date_index = date_index+temp[0:admin]
    #
	# 				# update show_number
	# 				show_number_item = admin
	# 				if show_number_item <= 0:
	# 					break
    #
	# 			last_tweet = collection_tweet.find_one({"id_str" : date_index[0][0]})
	# 			followers = last_tweet['user']['followers_count']
	# 			friends = last_tweet['user']['friends_count']
	# 			description = last_tweet['user']['description']
    #
	# 			# update user collection
	# 			collection_leader.update( { '_id': leader['_id'] },{ '$set': { "recent_tweet_ids": [ a[0] for a in date_index], 'followers': followers, 'friends':friends, 'description':description} } )
    #
	# 	print('>>> update_recent_info_by_tweets(show_number) ends!')


	# initial database
	def initial_database(self,show_number):

		# self.create_yaml_collection()
		# self.create_leaders_collection()
		# self.create_timeline_collection(collection_tweet.find())
		self.create_hashtag_collection(collection_tweet.find())
		# self.create_url_collection(collection_tweet.find())




if __name__ == '__main__':
	# link to followyourleaders_prod db in mongo
	print('>>> establishing mongo connection')
	MONGODB_HOST = 'localhost'
	MONGODB_PORT = 27018
	connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
	db = connection['followyourleaders_prod']

	# connect collection
	collection_yaml = db['yaml']		# yaml collection
	collection_tweet = db['tweets--drop']		# tweets collection
	collection_leader = db['leaders']		# leader collection
	collection_timeline = db['timelines'] # timeline collection (objectid, hashtags, time)
	collection_hashtags = db['hashtags'] # for updating tweets
	collection_url = db['urls'] # for urls

	# number of tweets show in recent tweets section
	show_number=10


	######################################### run here##########################################

	fyldb = followyourleaders()
	###################### When starting a new data base ########################################
	fyldb.initial_database(show_number)






	###################### when adding new data from collection tweet_new #########################
	#etl.update_database(show_number)

	connection.close()
