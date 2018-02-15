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
import yaml
from collections import defaultdict
import itertools
import requests


# define class
class followyourleaders(object):
	def __init__(self):
		self.a = 1


	############################ for creating yaml collection (will be dropped after the leader collection is built) #############################

	def create_yaml_collection(self):
		# reset yaml collection
		print('>>> create_yaml_collection() starts!')
		collection_yaml.drop()

		# read yaml files
		print('>>> reading yaml files')
		legislators_file = urllib.request.urlopen('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml')
		lst_a = yaml.load(legislators_file)
		media = urllib.request.urlopen('https://theunitedstates.io/congress-legislators/legislators-social-media.yaml')
		lst_b = yaml.load(media)


		# merge yaml files
		lst = sorted(itertools.chain(lst_b,lst_a), key=lambda x:x['id']['bioguide'])
		lst_legislators = []
		for k,v in itertools.groupby(lst, key=lambda x:x['id']['bioguide']):
		    d = {}
		    for dct in v:
		        d.update(dct)
		    lst_legislators.append(d)


		# insert into database
		for dct in lst_legislators:
			collection_yaml.insert(dct)
		print('>>> create_yaml_collection() ends!')


	############################# for creating leader collection and dropping yaml collection (source: yaml collection)#############################

	def create_leaders_collection (self) :
		print('>>> create_leaders_collection() starts!')

		# read from yamls collection
		yamls = collection_yaml.find()
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
						if 'twitter_id' in yaml['social']:
							twitter_id = str(yaml['social']['twitter_id'])
						else:
							twitter_id = 'NA'

						photo_url = requests.get('https://twitter.com/' + yaml['social']['twitter'] + '/profile_image?size=original').url

						# form data structure by datamodel.md
						leader_dict = {'twitter_name':yaml['social']['twitter'],'bioguide':yaml['id']['bioguide'],'twitter_id':twitter_id
						,'name':yaml['name']['official_full'],'gender':yaml['bio']['gender'],'birthday':yaml['bio']['birthday'],
						 'religion':religion,'state':state,'chamber':chamber,'party':party,'wikidata':yaml['id']['wikidata'],"photo_url":photo_url}

						# insert into database
						collection_leader.insert(leader_dict)


		# drop  yaml collection
		# collection_yaml.drop()
		print('>>> create_leaders_collection() ends!')



	############################# for creating initial database #############################
	
	def initial_database(self,show_number):

		self.create_yaml_collection()
		self.create_leaders_collection()





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
	show_number=10




	######################################### run here##########################################

	fyldb = followyourleaders()
	###################### When starting a new data base ########################################
	fyldb.initial_database(show_number)



	connection.close()
