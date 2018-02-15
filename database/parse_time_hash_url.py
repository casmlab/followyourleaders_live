__author__ = "Pai-ju Chang, Libby Hemphill"
__maintainer__ = "Pai-ju Chang"
__email__ = "paiju@umich.edu"
__status__ = "Development"

# Something here about what the code does


from pymongo import MongoClient
import pymongo
import json
import numpy as np
import pickle
import time
import urllib
from collections import defaultdict
import itertools
import requests


# define class
class followyourleaders(object):
	def __init__(self):
		self.a = 1


	############################ for creating timelines (source: tweets collection) #########################

	def create_timeline_collection(self, tweets):

		print('>>> create_timeline_collection(self, tweets) starts!')
		collection_timeline.drop()


		for tweet in tweets:

			leader = collection_leader.find_one({"twitter_id" : tweet['user']['id_str']})


			# check is or isnt this user a the leader
			if leader != None:

				# define date/time formats
				post_date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				post_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

				# create/update timelines collection
				leader_timeline = collection_timeline.find_one({"bioguide" : leader['bioguide']})

				# define update location
				keyidx = "dates."+post_date+"."+tweet['id_str']

				# define inserting/updating item format
				url = 'https://twitter.com/'+tweet['user']['screen_name']+'/status/'+tweet['id_str']
				item_push = {'hashtags': [a['text'] for a in tweet['entities']['hashtags']],'created_at':post_date_time,
				'url':url}


				# if we dont have the leader's information in timeline collection, insert one for him/her
				if  leader_timeline == None:

					print('start inserting '+leader['bioguide'] +' into timelines collection')
					dic={}
					dic['twitter_name']=tweet['user']['screen_name']
					dic['twitter_id']=tweet['user']['id_str']
					dic['bioguide']=leader['bioguide']
					dic.setdefault('dates', {})
					collection_timeline.insert(dic)


				# update timeline collection from tweets
				collection_timeline.update( { 'bioguide': leader['bioguide']},{ '$set': { keyidx: item_push } } )


		print('>>> create_timeline_collection(self, tweets) ends!')


	############################  function for creating hashtags collections  #########################

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

					print('start inserting ' + leader['bioguide'] + ' into hashtags collection')
					dic = {}
					dic['bioguide'] = leader['bioguide']
					dic.setdefault('hashtags', {})
					collection_hashtags.insert(dic)


				# update hashtags collection from tweets
				for a in tweet['entities']['hashtags']:

					key_idx = "hashtags." + a['text'] + ".tweets." + tweet['id_str']
					collection_hashtags.update({ 'bioguide': leader }, { '$set': {key_idx+'.text':tweet['text'],key_idx + '.created_at':post_date_time} } )


		print('>>> create_hashtags_collection(self, tweets) ends!')


	#############################  function for creating/updaing urls collections#########################
	def create_url_collection(self,tweets):

		print('>>> create_url_collection(self, tweets) starts!')
		collection_url.drop()


		for tweet in tweets:

			leader = collection_leader.find_one({"twitter_id" : tweet['user']['id_str']})


			# check is or isnt this user a the leader
			if leader != None:

				# define date/time formats
				post_date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				post_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

				# read leader's information from urls collection
				leader_url = collection_url.find_one({"bioguide" : leader})


				# if we dont have the leader's information in urls collection, insert one for him/her
				if leader_url == None:

					print('start inserting ' + leader['bioguide'] + ' into urls collection')
					dic = {}
					dic['bioguide'] = leader['bioguide']
					dic.setdefault('urls', {})
					collection_url.insert(dic)


				#update urls collection from tweets
				for a in tweet['entities']['urls']:

					key_idx = "urls." + a['url'].split("t.co/")[1] + ".tweets." + tweet['id_str']
					collection_url.update( { 'bioguide': leader },{ '$set': {key_idx + '.text':tweet['text'], key_idx + '.created_at':post_date_time} } )


		print('>>> create_url_collection(self, tweets) ends!')


	#############for updating "recent_tweets", "followers", "friends", "description" in leader collection (by timeline, tweets, leaders collections)#############################
	def update_leaders(self,num_tweets_shown):
		print('>>> update_leaders(num_tweets_shown) starts!')

		# load data from leader collection
		leaders = collection_leader.find()


		for leader in leaders:

			date_index = []
			text_index = []

			# check whether we have his/her Twitter data
			time_item = collection_timeline.find_one({"bioguide" : leader['bioguide']})


			# if we have this leader's data
			if time_item != None:

				a = time_item['dates'].keys()

				# sort by time https://stackoverflow.com/questions/5166842/sort-dates-in-python-array
				a.sort(key = lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")),reverse=True)
				#print(a)

				for u in a:

					sublist = time_item['dates'][u]
					temp = [(key,value['created_at']) for key,value in sublist.items()]

					temp.sort(key = lambda x: time.mktime(time.strptime(x[1],"%Y-%m-%d %H:%M:%S")),reverse=True)

					# decide #twitter we need to insert
					add_min = min(len(sublist),num_tweets_shown)
					date_index = date_index+temp[0:add_min]

					# update num_tweets_shown
					num_tweets_shown = add_min
					if num_tweets_shown <= 0:
						break

				last_tweet = collection_tweet.find_one({"id_str" : date_index[0][0]})
				followers = last_tweet['user']['followers_count']
				friends = last_tweet['user']['friends_count']
				description = last_tweet['user']['description']

				# update user collection
				collection_leader.update( { '_id': leader['_id'] },{ '$set': { "recent_tweet_ids": [ a[0] for a in date_index], 'followers': followers, 'friends':friends, 'description':description} } )

		print('>>> update_leaders(num_tweets_shown) ends!')



	############################# for creating initial database #############################

	def initial_database(self,num_tweets_shown):

		# self.create_timeline_collection(collection_tweet.find())
		# self.create_hashtag_collection(collection_tweet.find())
		# self.create_url_collection(collection_tweet.find())
		self.update_leaders(num_tweets_shown)






if __name__ == '__main__':
	# link to followyourleaders_prod db in mongo
	print('>>> establishing mongo connection')
	MONGODB_HOST = 'localhost'
	MONGODB_PORT = 27018
	connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
	db = connection['followyourleaders_prod']

	# connect collection
	collection_tweet = db['tweets--drop']		# tweets collection
	collection_leader = db['leaders']		# leader collection
	collection_timeline = db['timelines'] # timeline collection (objectid, hashtags, time)
	collection_hashtags = db['hashtags'] # for updating tweets
	collection_url = db['urls'] # for urls

	# number of tweets show in recent tweets section
	num_tweets_shown=10


	######################################### run here##########################################

	fyldb = followyourleaders()
	###################### When starting a new data base ########################################
	fyldb.initial_database(num_tweets_shown)






	###################### when adding new data from collection tweet_new #########################
	#etl.update_database(num_tweets_shown)

	connection.close()
