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

app = Flask('fyl')
mongo = PyMongo(app)

##############################################################
# For /legislator_detail/<legislator>

def load_legislator_details(user):
	details = {}

	user_dic = mongo.db.user_recent_tweets.find_one({"wikidata":user})

	details['bio'] = {}
	details['bio']['birthday'] = user_dic['birthday']
	details['bio']['religion'] = user_dic['religion']
	details['bio']['gender'] = user_dic['gender']
	details['id'] = {}
	details['id']['name'] = user_dic['name']
	details['terms'] = {}
	details['terms']['state'] = user_dic['state']
	details['terms']['type'] = user_dic['type']
	details['terms']['party'] = user_dic['party']
	details['recent_tweets'] = {}
	details['recent_tweets_li'] = user_dic['recent_tweets']

	return details



##############################################################
# For /compare_result

# function for loading data of the different type of tweets 
def load_sentiment_fuc(user="Ken Calvert") :

	sentiment = {}
	sentiment_dic = mongo.db.sentiment.find_one({"name":user})

	sentiment['Narrative'] = sentiment_dic['Narrative']
	sentiment['Other'] = sentiment_dic['Other']
	sentiment['Position'] = sentiment_dic['Position']
	sentiment['Provinfo'] = sentiment_dic['Provinfo']
	sentiment['Reqaction'] = sentiment_dic['Reqaction']
	sentiment['Thanks'] = sentiment_dic['Thanks']
	return sentiment


def load_sentiment(user0="Ken Calvert", user1="Joaquin Castro"):

	return load_sentiment_fuc(user0), load_sentiment_fuc(user1)


# function for loading data for tenure of leader

def load_tenure_fuc(user="Ken Calvert") :
	user_profile = mongo.db.yaml.find_one({"name.official_full":user})

	if user_profile:
		tenure = {}
		tenure['name'] = user_profile['name']['official_full']
		tenure['start'] , tenure['end']= {}, {}
		tenure['start']['year'],tenure['start']['month'],tenure['start']['day'] =  map(int, user_profile['terms'][0]['start'].split('-'))
		tenure['end']['year'],tenure['end']['month'],tenure['end']['day'] = d = map(int,user_profile['terms'][-1]['end'].split('-'))
	return tenure

def load_tenure(user0="Ken Calvert", user1="Joaquin Castro"):
	return load_tenure_fuc(user0), load_tenure_fuc(user1)


# function for loading the basic information of leader
def load_basic_info_fuc(user="Ken Calvert"):
		basic = {}
		userProfile = mongo.db.yaml.find_one({"name.official_full":user})

		if userProfile:
			basic['bio'] = {}
			basic['bio']['birthday'] = userProfile['bio']['birthday']
			basic['terms'] = {}
			basic['terms']['state'] = userProfile['terms'][0]['state']
			basic['terms']['type'] = 'house' if userProfile['terms'][0]['type'] == 'rep' else 'senate'
			basic['terms']['party'] = userProfile['terms'][0]['party']
			basic['twitter']=""
		if userProfile['social']:
			if userProfile['social']['twitter']:
				basic['twitter']=userProfile['social']['twitter']
				# imagine url redirected
				basic['twitter_url']=requests.get('https://twitter.com/'+userProfile['social']['twitter']+'/profile_image?size=original').url
		return basic


def load_basic_info(user0="Ken Calvert", user1="Joaquin Castro"):

	return load_basic_info_fuc(user0), load_basic_info_fuc(user1)


# function for loading the time series data (#Tweets)
def load_timeserie_fuc(user="Ken Calvert"):

	return mongo.db.timelines.find_one({"name":user})["time_counts"]

def load_timeserie(user0="Ken Calvert", user1="Joaquin Castro"):

	return load_timeserie_fuc(user0),load_timeserie_fuc(user1)



# function for loading the time line data (#Tweets)
def load_timeline_fuc(user="Ken Calvert"):
	timelines = mongo.db.timelines.find_one({"name":user})["time_counts"].keys()
	timelines=map(lambda v : datetime.strptime(v, '%b %d %Y').strftime('%Y%m'), timelines)
	timelines = list(set(sorted(map(int,timelines))))
	return sorted(list(findContiMonth(timelines)))


def load_timeline(user0="Ken Calvert", user1="Joaquin Castro"):

	return load_timeline_fuc(user0),load_timeline_fuc(user1)



# function for loading word count data (#Tweets)
def load_wordfreq_fuc(user="Ken Calvert"):
	wordfreq = mongo.db.wordfreqs.find_one({"name":user})["wordfreq"]
	wordfreq_li = sorted(wordfreq.items(), key=operator.itemgetter(1), reverse=True)
	return wordfreq_li[:10]

def load_wordfreq(user0="Ken Calvert", user1="Joaquin Castro"):
	return load_wordfreq_fuc(user0), load_wordfreq_fuc(user1)



def findContiMonth(L):
    first = last = L[0]
    for n in L[1:]:
        if n - 1 == last: # Part of the group, bump the end
            last = n
        else: # Not part of the group, yield current group and start a new
            yield first, last
            first = last = n
    yield first, last # Yield the last group