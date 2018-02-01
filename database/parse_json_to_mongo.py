__author__ = "Pai-ju Chang, Libby Hemphill"
__maintainer__ = "Pai-ju Chang"
__email__ = "paiju@umich.edu"
__status__ = "Development"

# Something here about what the code does

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
import requests 



# define class
class fyl_etl(object):
	def __init__(self):
		self.a = 1


	############################# for creating yaml collection ( will be dropped after the leader collection is built)############################# 
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


	############################# for creating leader collection and dropping yaml collection (source: yaml collection)############################# 
	############################# this leader collection is not completed, the recent tweets, followers, friends and description need ###############
	############################# to be updated by update_recent_info_by_tweets function ###########################################################
	def create_leaders_collection (self) :
		print('>>> create_leaders_collection() starts!')
		
		# read from yamls collection
		yamls= collection_yaml.find()
		collection_leader.drop()

		for yaml in yamls:
			# if this leader has used social media
			if 'social' in yaml:
				# if this leader has used twitter
				if 'twitter' in yaml['social']:
					# if this leader is in yamls.
					if 'bio' in yaml: 

						if 'religion' in yaml['bio']:
							religion = yaml['bio']['religion']
						else:
							religion = 'Unknown'
						state = yaml['terms'][0]['state']
						chamber =  yaml['terms'][0]['type']
						party = yaml['terms'][0]['party']
						twitter_id=str(yaml['social']['twitter_id'])
						photo_url =requests.get('https://twitter.com/'+yaml['social']['twitter']+'/profile_image?size=original').url
						
						# form data structure by datamodel.md
						leader_dict= {'twitter_name':yaml['social']['twitter'],'bioguide':yaml['id']['bioguide'],'twitter_id':twitter_id
						,'name':yaml['name']['official_full'],'gender':yaml['bio']['gender'],'birthday':yaml['bio']['birthday'],
						 'religion':religion,'state':state,'chamber':chamber,'party':party,'wikidata':yaml['id']['wikidata'],"photo_url":photo_url}
						collection_leader.insert(leader_dict)

		# drop  yaml collection
		#collection_yaml.drop()
		print('>>> create_leaders_collection() ends!')


	############################# for creating timelines, hashtages, urls collections(starting new) (source: tweets collection)#########################

	def create_time_hash_url_collection(self):

		print('>>> create_time_hash_url_collection() starts!')
		#reset collection_tweet collections
		collection_timeline.drop()
		collection_url.drop()
		collection_hashtage.drop()

		# run function to update/add timeline collection from tweets collection
		self.func_time_hash_url(collection_tweet.find())
		print('>>> create_time_hash_url_collection() ends!')

	###### for updating timelines, hashtages, urls collections(do not delete the old collections) form tweets_new collection (source: tweets_new collection)####

	def update_time_hash_url_collection(self):

		print('>>> update_time_hash_url_collection() starts!')
		# run function to update/add timeline collection from tweets_new collection
		self.func_time_hash_url(collection_tweetNew.find())

		# add data from tweets_new  to tweet collection, then dump the tweets_new collection
		self.move_tweetNew_to_tweet()
		print('>>> update_time_hash_url_collection() ends!')


	############################# excuting funcions for creating/updaing timelines, hashtages, urls collections#########################

	def func_time_hash_url(self, tweets):

		print('>>> func_time_hash_url(self, tweets) starts!')
		count=[]
		for tweet in tweets:

			leader=collection_leader.find_one({"twitter_id" : tweet['user']['id_str']})

			#check is or isnt this user a the leader
			# Yes
			if leader != None:

				# define date/time formats
				post_date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				post_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				
				#create/update timelines collection
				self.func_time(tweet,leader['bioguide'],post_date,post_date_time)
				#create/update hashtages collection
				self.func_hash(tweet,leader['bioguide'],post_date_time)
				#create/update urls collection
				self.func_url(tweet,leader['bioguide'],post_date_time)

				# count.append(tweet['user']['id_str'])
				# if len(count)>=10:
				# 	break
		print('>>> func_time_hash_url(self, tweets) ends!')

	#############################  funcion for creating/updaing timelines collections#########################	

	def func_time(self,tweet,leader,post_date,post_date_time):

		# read leader's information from timelines collection
		leader_timeline= collection_timeline.find_one({"bioguide" : leader})

		# define update location	
		keyinde="dates."+post_date+"."+tweet['id_str']

		# define inserting/updating item format
		url='https://twitter.com/'+tweet['user']['screen_name']+'/status/'+tweet['id_str']	
		item_push= {'hashtages': [a['text'] for a in tweet['entities']['hashtags']],'created_at':post_date_time,
		'url':url}

		################## check if the leader is already in timelines collection######################
		# if we dont have the leader's information in timeline collection, insert one for him/her
		if  leader_timeline == None:

			print 'start inserting '+leader +' into timelines collection'
			dic={}
			dic['twitter_name']=tweet['user']['screen_name']
			dic['twitter_id']=tweet['user']['id_str']
			dic['bioguide']=leader
			dic.setdefault('dates', {})
			collection_timeline.insert(dic)


		#update timeline collection from tweets
		collection_timeline.update( { 'bioguide': leader},{ '$set': { keyinde: item_push } } )
				

	#############################  funcion for creating/updaing hashtages collections#########################	

	def func_hash (self,tweet,leader,post_date_time):

		# read leader's information from hashtages collection
		leader_hashtage=collection_hashtage.find_one({"bioguide" : leader})

		################## check if the leader is already in hashtages collection######################
		# if we dont have the leader's information in hashtages collection, insert one for him/her
		if leader_hashtage==None:

			print 'start inserting '+leader +' into hashtages collection'
			dic={}
			dic['bioguide']=leader
			dic.setdefault('hashtags', {})
			collection_hashtage.insert(dic)

		#update hashtages collection from tweets
		for a in tweet['entities']['hashtags']:
			keyinde="hashtags."+a['text']+".tweets."+tweet['id_str']
			collection_hashtage.update( { 'bioguide': leader },{ '$set': {keyinde+'.text':tweet['text'],keyinde+'.created_at':post_date_time} } )


	#############################  funcion for creating/updaing urls collections#########################	
	def func_url (self,tweet,leader,post_date_time):

		# read leader's information from urls collection
		leader_url=collection_url.find_one({"bioguide" : leader})

		################## check if the leader is already in urls collection######################
		# if we dont have the leader's information in urls collection, insert one for him/her
		if leader_url==None:

			print 'start inserting '+leader +' into urls collection'
			dic={}
			dic['bioguide']=leader
			dic.setdefault('urls', {})
			collection_url.insert(dic)


		#update urls collection from tweets
		for a in tweet['entities']['urls']:
			#keyinde="urls."+a['url'].replace('.', '\u002e')+".tweets."+tweet['id_str']
			# print a['url'].split("t.co/")
			keyinde="urls."+a['url'].split("t.co/")[1] +".tweets."+tweet['id_str']
			collection_url.update( { 'bioguide': leader },{ '$set': {keyinde+'.text':tweet['text'],keyinde+'.created_at':post_date_time} } )



	#############################  move data from tweetNew to tweets collection, then drop the tweetNew collection ############################# 
	def move_tweetNew_to_tweet(self):

		print('>>> move_tweetNew_to_tweet() starts!')

		tweets = collection_tweetNew.find()
		for tweet in tweets:
			collection_tweet.insert(tweet)
		# when finishing, drop the database
		collection_tweetNew.drop()
		print('>>> move_tweetNew_to_tweet() ends!')



	#############for updating "recent_tweets", "followers", "friends", "description" in leader collection (by timeline, tweets, leaders collections)############################# 
	def update_recent_info_by_tweets(self,show_number):
		print('>>> update_recent_info_by_tweets(show_number) starts!')

		# load data from leader collection
		leaders = collection_leader.find()

		for leader in leaders:

			show_number_item=show_number			
			date_index=[]
			text_index=[]

			# check whether we have his/her Twitter data
			item=collection_timeline.find_one({"bioguide" : leader['bioguide']})
			


			# if we have this leader's data
			if item != None:

				a=item['dates'].keys()
				
				# sort by time https://stackoverflow.com/questions/5166842/sort-dates-in-python-array
				a.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")),reverse=True)
				#print a

				for u in a:
				
					sublist=item['dates'][u]
					temp=[(key,value['created_at']) for key,value in sublist.items()]
					
					temp.sort(key=lambda x: time.mktime(time.strptime(x[1],"%Y-%m-%d %H:%M:%S")),reverse=True)
					
					# decide #twitter we need to insert 
					addmin=min(len(sublist),show_number_item)
					date_index=date_index+temp[0:addmin]

					# update show_number
					show_number_item=show_number_item-addmin
					if show_number_item<=0:
						break

				last_tweet= collection_tweet.find_one({"id_str" : date_index[0][0]})
				followers=last_tweet['user']['followers_count']
				friends=last_tweet['user']['friends_count']
				description=last_tweet['user']['description']

				# update user collection	
				collection_leader.update( { '_id': leader['_id'] },{ '$set': { "recent_tweet_ids": [ a[0] for a in date_index], 'followers': followers, 'friends':friends, 'description':description} } )

		print('>>> update_recent_info_by_tweets(show_number) ends!')


	# initial database
	def initial_database(self,show_number):

		self.create_yaml_collection()
		self.create_leaders_collection()
		self.create_time_hash_url_collection()
		self.update_recent_info_by_tweets(show_number)



	# updating database from tweetNew collections:
	def update_database(self,show_number):

		self.update_time_hash_url_collection()
		self.update_recent_info_by_tweets(show_number)



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
	collection_leader = collection['leaders']		# leader collection
	collection_timeline = collection['timelines'] # timeline collection (objectid, hashtage, time)
	collection_tweetNew=collection['tweets_new'] # for updating tweets 
	collection_hashtage=collection['hashtages'] # for updating tweets 
	collection_url=collection['urls'] # for urls

	# number of tweets show in recent tweets section
	show_number=10


	######################################### run here##########################################

	etl = fyl_etl()
	###################### When starting a new data base ########################################
	etl.initial_database(show_number)
	
	




	###################### when adding new data from collection tweet_new #########################
	#etl.update_database(show_number)

	connection.close()