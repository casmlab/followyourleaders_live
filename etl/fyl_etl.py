from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
import re
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
import pickle
import yaml
import urllib

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection['fyl']
collection_tweet = collection['tweets']
collection_user_test = collection['users_test']
collection_new = collection['tweets_new']
collection_user = collection['users']
collection_timeline = collection['timelines']
collection_wordfreq = collection['wordfreqs']
collection_sentiment = collection['sentiment']
collection_user_recent_tweets = collection['user_recent_tweets']


class fyl_etl(object):
	def __init__(self):
		self.a = 1

	def sentiment_fresh(self):
		print('>>> sentiment_fresh() starts!')
		collection_sentiment.drop()

		target_names = ['Narrative', 'Other', 'Position', 'Provinfo', 'Reqaction', 'Thanks']

		user_li = []

		classifier = pickle.load(open('classifier.ml', 'rb'))
		sentiment_dicts = []

		tweets = collection_tweet.find()
		for tweet in tweets:
			user = tweet['user']['name']
			text = tweet['text']
			X_test_li = [text]
			X_test = np.array(X_test_li)
			predicted = classifier.predict(X_test)[0]
			#print(type(predicted))
			#for item, labels in zip(X_test, predicted):
			#	print '%s => %s' % (item, ', '.join(target_names[x] for x in labels))

			if user not in user_li:
				if target_names.index('Narrative') in predicted:
					sentiment_dict = {'name': user, 'Narrative': 1, 'Other': 0, 'Position': 0, 'Provinfo': 0, 'Reqaction': 0, 'Thanks': 0}
				if target_names.index('Position') in predicted:
					sentiment_dict = {'name': user, 'Narrative': 0, 'Other': 0, 'Position': 1, 'Provinfo': 0, 'Reqaction': 0, 'Thanks': 0}
				if target_names.index('Provinfo') in predicted:
					sentiment_dict = {'name': user, 'Narrative': 0, 'Other': 0, 'Position': 0, 'Provinfo': 1, 'Reqaction': 0, 'Thanks': 0}
				if target_names.index('Reqaction') in predicted:
					sentiment_dict = {'name': user, 'Narrative': 0, 'Other': 0, 'Position': 0, 'Provinfo': 0, 'Reqaction': 1, 'Thanks': 0}
				if target_names.index('Thanks') in predicted:
					sentiment_dict = {'name': user, 'Narrative': 0, 'Other': 0, 'Position': 0, 'Provinfo': 0, 'Reqaction': 0, 'Thanks': 1}
				if target_names.index('Other') in predicted:
					sentiment_dict = {'name': user, 'Narrative': 0, 'Other': 1, 'Position': 0, 'Provinfo': 0, 'Reqaction': 0, 'Thanks': 0}

				user_li.append(user)
				#print sentiment_dict
				#collection_sentiment.insert_one(sentiment_dict)
				sentiment_dicts.append(sentiment_dict.copy())
			else:
				#collection_timeline.delete_one({'name':username})
				#sentiment_dict = collection_sentiment.find_one({'name':user})
				for x in sentiment_dicts:
					if x['name'] == user:
						sentiment_dict = x
						break
				if target_names.index('Narrative') in predicted:
					sentiment_dict['Narrative'] += 1
				if target_names.index('Position') in predicted:
					sentiment_dict['Position'] += 1
				if target_names.index('Provinfo') in predicted:
					sentiment_dict['Provinfo'] += 1
				if target_names.index('Reqaction') in predicted:
					sentiment_dict['Reqaction'] += 1
				if target_names.index('Thanks') in predicted:
					sentiment_dict['Thanks'] += 1
				if target_names.index('Other') in predicted:
					sentiment_dict['Other'] += 1

				#collection_sentiment.delete_one({'name':user})
				#collection_sentiment.insert_one(sentiment_dict.copy())
			#print sentiment_dict

		collection_sentiment.insert(sentiment_dicts)

	def user_info_recent_tweets_fresh(self):
		print('>>> user_info_recent_tweets_fresh() starts!')
		collection_user_recent_tweets.drop()	
		user_li = []
		users = collection_user_test.find()

		month_li = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

		for user in users:
			bioguide = user['bioguide']
			description = user['description']
			birthday = user['birthday']
			wikidata = user['wikidata']
			name = user['name']
			gender = user['gender']
			religion = user['religion']
			state = user['state']
			twitter_name = user['twitter_name']
			party = user['party']
			type = user['type']

			#tweets = list(collection_tweet.find({'user.screen_name': user['twitter_name']}, {'user.created_at': 1, 'text': 1}).sort({'user.created_at', -1}).limit(10))
			tweets = list(collection_tweet.find({'user.screen_name': user['twitter_name']}, {'created_at': 1, 'text': 1, '_id': 0}).limit(10))
			
			if len(tweets) == 0:
					tweets_date_text = [[None, None]]	
			else:
				tweets_date_text = [[x['created_at'], x['text']] for x in tweets]
				
		
				#tweets_date_text = sorted(tweets_date_text, key=lambda x: x[2])[:10]
			

			if user and user not in user_li:
				user_dict = {'name': name, 'twitter_name': twitter_name, 'wikidata': wikidata, 'description': description, 'bioguide': bioguide, 'gender': gender, 'birthday': birthday, 'religion': religion, 'state': state, 'type': type, 'party': party, 'recent_tweets': tweets_date_text}
				user_li.append(user)
				collection_user_recent_tweets.insert_one(user_dict)
		
		print('>>> user_info_recent_tweets_fresh() completes!')

	def user_info_fresh(self):
		print('>>> user_info_fresh() starts!')
		collection_user_test.drop()	
		user_li = []
		tweets = collection_tweet.find()

		bioguide = None
		user = None
		twitter_name = None
		wikidata = None
		description = None
		gender = None
		birthday = None
		religion = None
		state = None
		type = None
		party = None

		recent_tweets = {}

		legislators_file = urllib.urlopen('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml')
		legislators_obj = yaml.load(legislators_file)
		legislators_file.close()

		social_media_file = urllib.urlopen('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-social-media.yaml')
		social_media_obj = yaml.load(social_media_file)
		social_media_file.close()

		for tweet in tweets:
			twitter_name = tweet['user']['screen_name']
			description = tweet['user']['description']
			
			for item in social_media_obj:
				if 'twitter' in item['social'] and item['social']['twitter'] == twitter_name:
					bioguide = item['id']['bioguide']
					break


			for item in legislators_obj:
				if item['id']['bioguide'] == bioguide:
					user = item['name']['official_full']
					wikidata = item['id']['wikidata']
					gender = item['bio']['gender']
					birthday = item['bio']['birthday']
					if 'religion' in item['bio']:
						religion = item['bio']['religion']
					else:
						religion = 'Unknown'
					state = item['terms'][0]['state']
					type = 'house' if item['terms'][0]['type'] == 'rep' else 'senate'
					party = item['terms'][0]['party']
				
					#tweets = list(collection_tweet.find({'user.screen_name': twitter_name}, {'user.created_at': 1, 'text': 1}).limit(10))
			
					#if len(tweets) == 0:
					#	tweets_date_text = [[None, None]]
					#elif len(tweets) == 1:
				
					#	tweets_date_text = [[x['user']['created_at'], x['text']] for x in tweets]
					#else:
					#	tweets_date_text = [[x['user']['created_at'], x['text']] for x in tweets]

					#break

			if user and user not in user_li:
				#user_dict = {'name': user, 'twitter_name': twitter_name, 'wikidata': wikidata, 'description': description, 'bioguide': bioguide, 'gender': gender, 'birthday': birthday, 'religion': religion, 'state': state, 'type': type, 'party': party, 'recent_tweets': tweets_date_text}
				user_dict = {'name': user, 'twitter_name': twitter_name, 'wikidata': wikidata, 'description': description, 'bioguide': bioguide, 'gender': gender, 'birthday': birthday, 'religion': religion, 'state': state, 'type': type, 'party': party}
				user_li.append(user)
				collection_user_test.insert_one(user_dict)

		print('>>> user_info_fresh() completed!')





	def user_info_append(self):
		print('>>> user_info_append() starts!')
		user_li = []
		tweets = collection_new.find()
		users = collection_user.find()
		for user in users:
			user_li.append(user['name'])

		for tweet in tweets:
			new_user = tweet['user']['name']
			description = tweet['user']['description']

			while '.' in new_user:
				i = new_user.index('.')
				new_user = new_user[:i]+new_user[i+1:]
                
			if new_user not in user_li:
				user_dict = {'name': new_user, 'description': description}
				user_li.append(new_user)
				collection_user.insert_one(user_dict)

			# Combine tweets_new collections with the tweets collection
			collection_tweet.insert(tweet)
			collection_new.drop()
			
		print('>>> user_info_append() completed!')

	def timeline_fresh(self):
		print('>>> timeline_fresh() starts!')
		collection_timeline.drop()
		timelines = []
		tweets = collection_tweet.find()

		for tweet in tweets:
			# Extract user name
			username = tweet['user']['name']
			screen_name = tweet['user']['screen_name']
			# Extract created time
			created_at = tweet['created_at'].split()
			created_at = ' '.join(created_at[1:3] + [created_at[-1]])
			# Clean user name
			#while '.' in username:
			#	i = username.index('.')
			#	username = username[:i]+username[i+1:]	
			time_line_exists = None
			time_count_exists = None
	
			for timeline in timelines:
				if timeline['name'] == username:
					time_line_exists = True
					if created_at in timeline['time_counts']:		
						timeline['time_counts'][created_at] += 1
						break
					else:
						timeline['time_counts'][created_at] = 1	
					break
			if not time_line_exists:
				timelines.append({'name': username, 'scree_nname': screen_name, 'time_counts':{}})

		for timeline in timelines:
			collection_timeline.insert_one(timeline)

		print('>>> timeline_fresh() completed!')

	def timeline_append(self):
		print('>>> timeline_append() starts!')	
		tweets = collection_new.find()
 
		for tweet in tweets:
			username = tweet['user']['name']
			created_at = tweet['created_at'].split()
			created_at = ' '.join(created_at[1:3] + [created_at[-1]])
			while '.' in username:
				i = username.index('.')
				user = username[:i]+username[i+1:]
			
			timelines = collection_timeline.find({'name':username})
			# New user!
			if timelines.count() == 0:
				collection_timeline.insert_one({'name':username, 'time_counts':{created_at : 1}})
			# User already in timeline!
			else:
				for timeline in timelines:	
					# Old user, new time!
					if created_at not in timeline['time_counts']:	
						timeline['time_counts'][created_at] = 1
						collection_timeline.delete_one({'name':username})
						collection_timeline.insert_one(timeline)
					# User exists, time slot exists too!
					else:
						timeline['time_counts'][created_at] += 1
						collection_timeline.delete_one({'name':username})
						collection_timeline.insert_one(timeline)				

		print('>>> timeline_append() completed!')

	def wordfreq_fresh(self):
		print('>>> wordfreq_fresh() starts!')
		collection_wordfreq.drop()
		# Load the stop words
		with open('stop_words.txt') as file:
			stopwords = file.read().splitlines()

		wordfreqs = {}
		tweets = collection_tweet.find()
		
		for tweet in tweets:
			user = tweet['user']['name']
			words = tweet['text'].split()
			for word in words:
				word = re.sub('[!.,:@#$]', '', word)
				if word not in stopwords:
					while '.' in user:
						i = user.index('.')
						user = user[:i]+user[i+1:]
					if user not in wordfreqs:
						wordfreqs[user] = {}
					elif word not in wordfreqs[user]:
						wordfreqs[user][word] = 1
					else:
						wordfreqs[user][word] += 1

		for user in wordfreqs:
			collection_wordfreq.insert_one({'name': user, 'wordfreq': wordfreqs[user]})

		print('>>> wordfreq_fresh() completed!')

	def wordfreq_append(self):
		print('>>> wordfreq_append() starts!')
		# Load the stop words
		with open('stop_words.txt') as file:
			stopwords = file.read().splitlines()

		tweets = collection_new.find()

		for tweet in tweets:
			user = tweet['user']['name']
			words = tweet['text'].split()
			for word in words:
				word = re.sub('[!.,:@#$]', '', word)
				if word not in stopwords:
					while '.' in user:
						i = user.index('.')
						user = user[:i]+user[i+1:]

					wordfreqs = collection_wordfreq.find({'name': user})
					if wordfreqs.count() == 0:
						collection_wordfreq.insert_one({'name':user, 'wordfreq':{}})
					else:				
						for wordfreq in wordfreqs:
							if word in wordfreq['wordfreq']:
								wordfreq['wordfreq'][word] += 1
							else:
								wordfreq['wordfreq'][word] = 1
							collection_wordfreq.delete_one({'name': user})
							collection_wordfreq.insert_one(wordfreq)

		for user in wordfreqs:
			collection_wordfreq.insert_one({user : wordfreqs[user]})

		print('>>> wordfreq_append() completed!')

def main():
	#print(connection.collection_names())
	#print('users' in connection.collection_names())

	etl = fyl_etl()
	etl.user_info_recent_tweets_fresh()
	#etl.user_info_fresh()
	#etl.user_info_add_social()
	#etl.user_info_append()
	#etl.timeline_fresh()
	#etl.timeline_append()
	#etl.wordfreq_fresh()
	#etl.wordfreq_append()
	#etl.sentiment_fresh()
	#etl.legislator_fresh()
	connection.close()

if __name__ == '__main__':
	main()


