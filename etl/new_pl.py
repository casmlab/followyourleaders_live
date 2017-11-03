from pymongo import MongoClient
import pymongo
import json
from bson import json_util
from bson.json_util import dumps
#import re
import numpy as np
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.svm import LinearSVC
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.multiclass import OneVsRestClassifier
import pickle
import time
from bson.objectid import ObjectId
import urllib
import yaml
from collections import defaultdict
import itertools 



# define class
class fyl_etl(object):
	def __init__(self):
		self.a = 1


	############################# for creating yaml collection ############################# 
	def create_yaml_collection(self):
		# reset yaml collection
		print('>>> create_yaml_collection() starts!')
		collection_yaml.drop()

		#read yaml files
		legislators_file = urllib.urlopen('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml')
		list_a = yaml.load(legislators_file)
		media = urllib.urlopen('https://theunitedstates.io/congress-legislators/legislators-social-media.yaml')
		list_b = yaml.load(media)


		# merge yaml files
		lst = sorted(itertools.chain(list_b,list_a), key=lambda x:x['id']['bioguide'])
		list_c = []
		for k,v in itertools.groupby(lst, key=lambda x:x['id']['bioguide']):
		    d = {}
		    for dct in v:
		        d.update(dct)
		    list_c.append(d)

		# insert in database
		for i in list_c:
		    collection_yaml.insert(i)
		print('>>> create_yaml_collection() ends!')


	############################# for creating user collection (extracting attributes from yaml collection)############################# 
	def create_user_collection (self) :
		print('>>> create_user_collection() starts!')
		
		# read from yamls collection
		yamls= collection_yaml.find()
		collection_user.drop()

		for yaml in yamls:
			if 'social' in yaml:
				if 'twitter' in yaml['social']:
					if 'bio' in yaml: # make sure leader is included in both yamls

						if 'religion' in yaml['bio']:
							religion = yaml['bio']['religion']
						else:
							religion = 'Unknown'
						state = yaml['terms'][0]['state']
						type =  yaml['terms'][0]['type']
						party = yaml['terms'][0]['party']
						twitter_id=str(yaml['social']['twitter_id'])


						
						# yaml_dic.setdefault(twitter_id,{})
						# yaml_dic[twitter_id]= {'twitter_name':yaml['social']['twitter'],'bioguide':yaml['id']['bioguide']
						# ,'official_full':yaml['name']['official_full'],'gender':yaml['bio']['gender'],'birdthday':yaml['bio']['birthday'],
						#  'religion':religion,'state':state,'type':type,'party':party,'wikidata':yaml['id']['wikidata']}

						user_dict= {'twitter_name':yaml['social']['twitter'],'bioguide':yaml['id']['bioguide'],'twitter_id':twitter_id
						,'official_full':yaml['name']['official_full'],'gender':yaml['bio']['gender'],'birdthday':yaml['bio']['birthday'],
						 'religion':religion,'state':state,'type':type,'party':party,'wikidata':yaml['id']['wikidata']}
						collection_user.insert(user_dict)
					else:
						pass
		print('>>> create_user_collection() ends!')


	############################# for creating timeline collection tweets collection##########################

	def create_timeline_collection(self):

		print('>>> create_timeline_collection() starts!')
		#reset collection_tweet collections
		collection_timeline.drop()

		# run function to update/add timeline collection from tweets collection
		self.fun_creat_up_timeline(collection_tweet.find())
		print('>>> create_timeline_collection() ends!')

	############################# for updating timeline collection from tweetNew collection##########################

	def update_timeline_from_newTweets(self):

		print('>>> update_timeline_from_newTweets() starts!')
		# run function to update/add timeline collection from tweets_new collection
		self.fun_creat_up_timeline(collection_tweetNew.find())

		# add data from tweets_new  to tweet collection, then dump the tweets_new collection
		self.move_tweetNew_to_tweet()
		print('>>> update_timeline_from_newTweets() ends!')


	############################# funcion for creating/ updating timeline collection#########################

	def fun_creat_up_timeline(self, tweets):

		count=[]
		for tweet in tweets:

			# get twitter id and name
			twitter_name = tweet['user']['screen_name']
			twitter_id_str=tweet['user']['id_str']
			description=tweet['user']['description']


			#check is or isnt this user is the leader
			# if the user is leader
			if collection_user.find_one({"twitter_id" : twitter_id_str}) != None:

				leader=collection_timeline.find_one({"twitter_id" : twitter_id_str})

				# define time formats 			
				ts = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				ts_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))


				keyinde="time."+ts
				url='https://twitter.com/'+twitter_name+'/status/'+tweet['id_str']
				
				item_push= {'tweets_id':tweet['_id'],'hashtage': [a['text'] for a in tweet['entities']['hashtags']],'time':ts_time,
				'url':url}

				################## check if the leader is already in timeline collection######################
				# if it is a new leader
				if  leader == None:

					saveLine={}
					user=collection_user.find_one({"twitter_id" : twitter_id_str})
					print 'start inserting '+user['bioguide']
					
					saveLine['twitter_name']=twitter_name
					saveLine['twitter_id']=twitter_id_str
					saveLine['bioguide']=user['bioguide']
					saveLine['description']=description
					# save tweets by date
					saveLine.setdefault('time', {})
					saveLine['time'].setdefault(ts, [])
					saveLine['time'][ts].append( {'tweets_id':tweet['_id'],'hashtage': [a['text'] for a in tweet['entities']['hashtags']],'time':ts_time,
						'url':url})
					collection_timeline.insert(saveLine)

				# if it is a old leader in timeline collection
				else:
					#check if the date already in timeline collection
					if ts in leader['time']:
						collection_timeline.update( { '_id': leader['_id'] },{ '$push': { keyinde: item_push } } )
					else:
						collection_timeline.update( { '_id': leader['_id'] },{ '$set': { keyinde: [item_push] } } )
						


				# count.append(twitter_name)
				# if len(count)>1000:
				# 	break



	#############################  move data from tweetNew to tweets collection, then drop the tweetNew collection ############################# 
	def move_tweetNew_to_tweet(self):

		print('>>> move_tweetNew_to_tweet() starts!')

		tweets = collection_tweetNew.find()
		for tweet in tweets:
			collection_tweet.insert(tweet)
		# when finishing, drop the database
		collection_tweetNew.drop()
		print('>>> move_tweetNew_to_tweet() ends!')



	#############################  update "recent_tweets" in user collection (by timeline, tweets, user collections)############################# 
	def update_recent_tweets(self,show_number):
		print('>>> update_recent_tweets(show_number) starts!')

		# load data from user collection
		users = collection_user.find()


		for user in users:
			
			date_index=[]
			text_index=[]

			# check if the user is leader and we have his/her Twitter data
			item=collection_timeline.find_one({"bioguide" : user['bioguide']})


			# if not
			if item != None:
				a=item['time'].keys()
				
				# sort by time https://stackoverflow.com/questions/5166842/sort-dates-in-python-array
				a.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")),reverse=True)

				for u in a:
					sublist=item['time'][u]
					sublist.sort(key=lambda x: time.mktime(time.strptime(x['time'],"%Y-%m-%d %H:%M:%S")),reverse=True)

					# decide #twitter we need to insert 
					addmin=min(len(sublist),show_number)
					date_index=date_index+sublist[0:addmin]

					# update show_number
					show_number=show_number-addmin
					if show_number<=0:
						break

				# load the text from tweets collection
				for ind in date_index:
					text= collection_tweet.find_one({"_id" : ind['tweets_id']})
					text_index.append([ind['time'],text['text']])

				# update user collection
				collection_user.update( { '_id': user['_id'] },{ '$set': { "recent_tweets": text_index } } )
				print('>>> update_recent_tweets(show_number) ends!')





	# initial database
	def initial_database(self,show_number):

		self.create_yaml_collection()
		self.create_user_collection()
		self.create_timeline_collection()
		self.update_recent_tweets(show_number)


	# updating database from tweetNew collections:
	def update_database(self,show_number):

		self.update_timeline_from_newTweets()
		self.update_recent_tweets(show_number)


if __name__ == '__main__':
	#link to mongo and linke to fyl_Umich database
	MONGODB_HOST = 'localhost'
	MONGODB_PORT = 27017
	connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
	collection = connection['fyl_Umich']


	# connect collection
	collection = connection['fyl_Umich']
	collection_yaml = collection['yaml']		#yaml collection
	collection_tweet = collection['tweets']		# tweets collection
	collection_user = collection['users']		# users collection
	collection_timeline = collection['timeline'] # timeline collection (objectid, hashtage, time)
	collection_tweetNew=collection['tweets_new'] # for updating tweets 

	# number of tweets show in recent tweets section
	show_number=5




	######################################### run here##########################################

	etl = fyl_etl()
	###################### When starting a new data base ########################################
	etl.initial_database(show_number)

	###################### when adding new data from collection tweet_new #########################
	#etl.update_database(show_number)

	connection.close()

