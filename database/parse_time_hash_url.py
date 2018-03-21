__author__ = "Pai-ju Chang, Libby Hemphill"
__maintainer__ = "Angela Schöpke"
__email__ = "aschopke@umich.edu"
__status__ = "Development"

# CODE DESCRIPTION: This code creates a new 'timeline' collection, a new 'hashtags' collection, and a new 'urls' collection in 'followyourleaders_prod' database. 
# Important to note, each time these collections are created, the old ones (if they exist) are dropped. This code also updates existing 'leaders' collection in
# 'followyourleaders_prod' database with corresponding data from newly created 'timeline' collection.


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


	###################################################################    TIMELINE CREATION    ###############################################################

	
	# function definition: creates 'timeline' collection in 'followyourleaders_prod' database
	# source data: 	'leader' collection in 'followyourleaders_prod' database;
	#				'tweets--drop' collection in 'followyourleaders_prod' database;

	def update_timeline_collection(self, tweets):

		print('>>> update_timeline_collection(self, tweets) starts!')

		for tweet in tweets:

			if tweet['user']['id_str'] == "1155335864":
				leader = collection_leaders.find_one({"twitter_id" : tweet['user']['id_str']})
				# leader = collection_leaders.find_one({"twitter_id" : tweet['user']['id_str']})	

				# check whether the user that made the Tweet is a leader in collection_leaders or not
				if leader != None:

					# define date/time formats
					post_date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
					post_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

					# create/update timelines collection
					leader_timeline = collection_timeline.find_one({"bioguide" : leader['bioguide']})

					# define update location
					key_idx = "dates." + post_date + "." + tweet['id_str']

					try:
						val = leader_timeline['dates'][post_date][tweet['id_str']]['tweet_text']
						print('Already logged this Tweet.')
					except:
						print('Adding new Tweet.')
						# define inserting/updating item format
						text_push = tweet['text']
						url_push = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str']
						hash_push = [a['text'] for a in tweet['entities']['hashtags']]
						date_push = post_date_time


						# if we dont have the leader's information in timeline collection, insert the leader's information
						if  leader_timeline == None:

							print('start inserting ' + leader['bioguide'] + ' into timelines collection')
							dic = {}
							dic['twitter_name'] = tweet['user']['screen_name']
							dic['twitter_id'] = tweet['user']['id_str']
							dic['bioguide'] = leader['bioguide']
							dic.setdefault('dates', {})
							collection_timeline.insert(dic)


						# update specified leader's timeline collection from tweets
						collection_timeline.update({'bioguide': leader['bioguide']},{'$set': {key_idx: {'url':url_push, 'created_at': date_push, 'hashtags': hash_push, 'tweet_text':text_push}}})
			else:
				print("Not in here.")
		print('>>> update_timeline_collection(self, tweets) ends!')





	###################################################################    HASHTAG CREATION    ################################################################

	
	# function definition: creates 'hashtag' collection in 'followyourleaders_prod' database
	# source data: 	'leader' collection in 'followyourleaders_prod' database;
	#				'tweets--drop' collection in 'followyourleaders_prod' database;

	def update_hashtag_collection(self, tweets):

		print('>>> update_hashtags_collection(self, tweets) starts!')

		print(tweets)

		for tweet in tweets:
			leader = collection_leaders.find_one({"twitter_id" : tweet['user']['id_str']})
			print(leader)

			# check whether the user that made the Tweet is a leader in collection_leaders or not
			if leader != None:

				# define date/time formats
				post_date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				post_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

				leader_hashtags = collection_hashtags.find_one({'bioguide' : leader['bioguide']})
				
				# check if the leader is already in hashtags collection, if not, insert their information
				if leader_hashtags == None:

					print('start inserting ' + leader['bioguide'] + ' into hashtags collection')
					dic = {}
					dic['bioguide'] = leader['bioguide']
					dic.setdefault('hashtags', {})
					collection_hashtags.insert(dic)


				# update hashtags collection from tweets
				for a in tweet['entities']['hashtags']:

					key_idx = "hashtags." + a['text'] + ".tweets." + tweet['id_str']
					text_idx = key_idx + '.text'
					date_idx = key_idx + '.created_at'
					text_push = tweet['text']
					date_push = post_date_time

					
					try:
						val = leader_hashtags['hashtags'][a['text']]['tweets'][tweet['id_str']]
						print('Already logged this Tweet.')
					except:
						print('Adding new Tweets.')
						# define inserting/updating item format
						collection_hashtags.update({'bioguide':leader['bioguide']},{'$set':{text_idx:text_push,date_idx:date_push}})


		print('>>> update_hashtags_collection(self, tweets) ends!')





	###################################################################    URLS CREATION    ###################################################################
	

	# function definition: creates 'urls' collection in 'followyourleaders_prod' database
	# source data: 	'leader' collection in 'followyourleaders_prod' database;
	#				'tweets--drop' collection in 'followyourleaders_prod' database;

	def update_url_collection(self,tweets):

		print('>>> update_url_collection(self, tweets) starts!')

		for tweet in tweets:
			leader = collection_leaders.find_one({"twitter_id": tweet['user']['id_str']})

			# check whether the user that made the Tweet is a leader in collection_leaders or not
			if leader != None:

				# define date/time formats
				post_date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				post_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

				# read leader's information from urls collection
				leader_url = collection_url.find_one({"bioguide": leader['bioguide']})

				# if we dont have the leader's information in urls collection, if not, insert their information
				if leader_url == None:

					print('start inserting ' + leader['bioguide'] + ' into urls collection')
					dic = {}
					dic['bioguide'] = leader['bioguide']
					dic.setdefault('urls', {})
					collection_url.insert(dic)


				#update urls collection from tweets
				for a in tweet['entities']['urls']:

					key_idx = "urls." + a['url'].split("t.co/")[1] + ".tweets." + tweet['id_str']
					text_idx = key_idx + '.text'
					text_push = tweet['text']
					date_idx = key_idx + '.created_at'
					date_push = post_date_time

					try:
						val = leader_url['urls'][a['url'].split("t.co/")[1]]['tweets'][tweet['id_str']]
						print('Already logged this Tweet.')
					except:
						print('Adding new Tweets.')
						# define inserting/updating item format
						collection_url.update({'bioguide': leader['bioguide']},{'$set': {text_idx:text_push,date_idx:date_push}})


		print('>>> update_url_collection(self, tweets) ends!')





	###################################################################    UPDATE  LEADERS    #################################################################
	

	# function definition: updates 'leaders' collection in 'followyourleaders_prod' database with each leader's associated 'timeline' and 'tweets--drop' collection information
	# source data: 	'leader' collection in 'followyourleaders_prod' database;
	#				'timeline' collection in 'followyourleaders_prod' database;
	#				'tweets--drop' collection in 'followyourleaders_prod' database


	def update_leaders(self,num_tweets_shown):
		print('>>> update_leaders(num_tweets_shown) starts!')

		# load data from leader collection
		leaders = collection_leaders.find()

		for leader in leaders[200:]:

			date_index = []
			text_index = []

			# check whether we have his/her Twitter data
			time_item = collection_timeline.find_one({"bioguide" : leader['bioguide']})

			# if we have this leader's data
			if time_item != None:

				a = time_item['dates'].keys()
				
				lst_keys = [k for k in a]

				# sort by time https://stackoverflow.com/questions/5166842/sort-dates-in-python-array
				lst_keys.sort(key = lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")),reverse=True)

				for u in lst_keys:

					sublist = time_item['dates'][u]

					date_info = [(id_str,info['created_at']) for id_str,info in sublist.items()]
					try:
						text_info = [(id_str,info['tweet_text']) for id_str,info in sublist.items()]
					except:
						print(sublist.items())


					# decide #twitter we need to insert
					add_min = min(len(sublist),num_tweets_shown)
					

					date_index = date_index + date_info[0:add_min]
					text_index = text_index + text_info[0:add_min]

					num_tweets_shown = len(date_index)
					if num_tweets_shown >= 10:
						break

				
				# update num_tweets_shown
				last_tweet = collection_tweet.find_one({"id_str" : date_index[0][0]})
				followers = last_tweet['user']['followers_count']
				friends = last_tweet['user']['friends_count']
				description = last_tweet['user']['description']

				# update leader collection
				print("Updating with recent Tweet info.")
				collection_leaders.update({'_id': leader['_id']},{'$set': {'followers': followers, 'friends':friends, 'description':description, 'recent_tweets': {date_index[0][0] : {'created_at': date_index[0][1], 'tweet_text': text_index[0][1]}}, date_index[1][0] : {'created_at': date_index[1][1], 'tweet_text': text_index[1][1]},date_index[2][0] : {'created_at': date_index[2][1], 'tweet_text': text_index[2][1]},date_index[3][0] : {'created_at': date_index[3][1], 'tweet_text': text_index[3][1]}, date_index[4][0] : {'created_at': date_index[4][1], 'tweet_text': text_index[4][1]},date_index[5][0] : {'created_at': date_index[5][1], 'tweet_text': text_index[5][1]},date_index[6][0] : {'created_at': date_index[6][1], 'tweet_text': text_index[6][1]},date_index[7][0] : {'created_at': date_index[7][1], 'tweet_text': text_index[7][1]},date_index[8][0] : {'created_at': date_index[8][1], 'tweet_text': text_index[8][1]},date_index[9][0] : {'created_at': date_index[9][1], 'tweet_text': text_index[9][1]}}})


		print('>>> update_leaders(num_tweets_shown) ends!')


	#################################################################    INITIALIZING DB    ###################################################################

	
	# function definition: initializes database by calling each function defined in the followyourleaders() class
	# source data: 	'num_tweets_shown' parameter input in 'if __name__ == '__main__'' function
	#				'timeline' collection in 'followyourleaders_prod' database;
	#				'tweets--drop' collection in 'followyourleaders_prod' database

	def initialize_database(self,num_tweets_shown):

		
		self.update_timeline_collection(collection_tweet.find())
		# self.update_hashtag_collection(collection_tweet.find())
		# self.update_url_collection(collection_tweet.find())
		# self.update_leaders(num_tweets_shown)






#################################################################    RUN CODE HERE   ##########################################################################


if __name__ == '__main__':
	# link to followyourleaders_prod db in mongo
	print('>>> establishing mongo connection')
	MONGODB_HOST = 'localhost'
	MONGODB_PORT = 27018
	connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
	db = connection['followyourleaders_prod']
	
    
	# connect collection
	collection_tweet = db['tweets--drop']   # tweets collection
	collection_leaders = db['leaders']		# leader collection
	collection_timeline = db['timelines']   # timeline collection (objectid, hashtags, time)
	collection_hashtags = db['hashtags']    # for updating tweets
	collection_url = db['urls'] 			# for urls

	# number of tweets show in recent tweets section
	num_tweets_shown=10


	# initialize class instance
	fyldb = followyourleaders()
	# run functions in class

	fyldb.initialize_database(num_tweets_shown)



	connection.close()
