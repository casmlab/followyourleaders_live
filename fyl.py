import argparse
from data_load import *
from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
import json
from bson import json_util
from bson.json_util import dumps
import operator
import yaml
import urllib
from flask import request


app = Flask('fyl')
mongo = PyMongo(app)




@app.route("/")
def index():
	return render_template("index.html")


@app.route("/faq")
def faq():
	return render_template("faq.html")
	
@app.route("/legislators")
def leaders_list():
	users = mongo.db.user_recent_tweets.find()

	user_li = []
	for user in users:
		if user['type'] == 'house':
			type = 'Rep. '
		else:
			type = 'Sen. '

		if user['party'] == 'Republican':
			short = 'R-' + user['state']
		else:
			short = 'D-' + user['state']

		user_li.append([type+user['name']+' ('+short+')', user['description'],  user['wikidata']])

	user_li = sorted(user_li, key = lambda x: x[0].split()[1])

	#users_dict = {}
	#for user in users:
	#	users_dict[user['name']] = {'wikidata': user['wikidata'], 'description': user['description']}	
	#users_dict = {}
	#users_dict[user['name']]['description'] = user['description']
	#users_dict[user['name']]['wikidata'] = user['wikidata']

	return render_template("legislators.html", **locals())


# <legislator> here use ['id']['wikidata']
@app.route("/legislator_detail/<legislator>", methods=['GET'])
def leaders_details(legislator):
	details = load_legislator_details(legislator)

	

	return render_template("legislator_detail.html", **locals())


@app.route("/compare")
def comparisons():
	return render_template("compare_default.html")


@app.route("/compare_result")
def comparisons_result():
	# Load user names

	# read parameters from url
	#http://0.0.0.0:5000/compare_result?leader0=Sherrod%20Brown&leader1=Ken%20Calvert
	user0 = "Ken Calvert" if not request.args.get('leader0') else request.args.get('leader0')
	user1 = "Joaquin Castro" if not request.args.get('leader1') else request.args.get('leader1')

	# Load basic infos	
	basic0, basic1 = load_basic_info(user0, user1)
	# Load timelines
	timelines_0_dic, timelines_1_dic = load_timeline(user0, user1)
	# Load word frequencies
	wordfreq_0_li, wordfreq_1_li = load_wordfreq(user0, user1)
	# Load tenures
	tenure0, tenure1 = load_tenure(user0, user1)	
	# Load sentiment analysis
	sentiment0, sentiment1 = load_sentiment(user0, user1)

	return render_template("compare_result.html", **locals())	



@app.route("/leaderSingle")


def leaderSingle():
	# Load user names

	# read parameters from url
	#http://0.0.0.0:5000/compare_result?leader0=Sherrod%20Brown&leader1=Ken%20Calvert
	user = "Ken Calvert" if not request.args.get('leader0') else request.args.get('leader0')


	# Load basic infos	
	basic0 = load_basic_info_fuc(user)
	# Load timelines
	timelines_0_dic = load_timeline_fuc(user)
	# Load word frequencies
	wordfreq_0_li = load_wordfreq_fuc(user)
	# Load tenures
	tenure0 = load_tenure_fuc(user)	
	# Load sentiment analysis
	sentiment0 = load_sentiment_fuc(user)
	# time series analysis
	timeseries_0 = load_timeserie_fuc(user)


	return render_template("leaderSingle.html", **locals())	




if __name__ == "__main__":
	# Parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-m", help="mode")
	args = parser.parse_args()

	# Identify the mode
	if not args.m:
		args.m = 'norm'
	mode = args.m

	if mode == 'dev':
		app.run(host='0.0.0.0', port=5000, debug=True)
	else:
		app.run(host='0.0.0.0', debug=True)






