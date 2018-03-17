import argparse
from data_load import *
from flask import Flask
from flask import render_template, redirect, url_for, abort, jsonify
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
import json
from bson import json_util
from bson.json_util import dumps
import operator
import yaml
import urllib
from flask import request


# function for changing leaders' orders based on their parties
def changeOrder(leader0,leader1):
	if leader0 and leader1:
		if 'party' in leader0 and 'party' in leader1:
			if leader0['party'] == 'Republican':
				if leader1['party']=='Democrat' or leader1['party']=='Independent':
					return True

			if leader1['party'] == 'Democrat':
				if leader0['party']=='Republican' or leader0['party']=='Independent':
					return True
	return False

# function for loading leader data
def loadLeaderdata(leader_bio=None):
	if leader_bio:
		basic=load_basic_info_fuc(leader_bio)
		if basic:
			timeseries = load_timeserie_fuc(leader_bio)
			hashtags=load_hash_data(leader_bio)
			urls=load_url_data(leader_bio)
			return basic, timeseries, hashtags, urls
	return {}, {}, {}, {}


# routes
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/faq")
def faq():
	return render_template("faq.html")

@app.route("/leaders", methods=['GET'])
# @app.route("/leaders/<leader0>", methods=['GET'])
# @app.route("/leaders/<leader0>/<leader1>", methods=['GET'])
def leaders():
	leader0 = "H001061" if not request.args.get('leader0') else request.args.get('leader0')
	
	# Load leaders data from mongo	
	basic0, timeseries_0, hash_0, url_0 = loadLeaderdata(leader0)
	if request.args.get('leader1'):
		leader1=request.args.get('leader1')
		basic2, timeseries_2, hash_2, url_2 = loadLeaderdata(leader1)
		if changeOrder(basic0,basic2):
			basic0,basic2=basic2,basic0
			timeseries_0,timeseries_2=timeseries_2,timeseries_0
			hash_0,hash_2=hash_2,hash_0
			url_0,url_2=url_2,url_0
	else:
		basic2, timeseries_2, hash_2, url_2 = loadLeaderdata()
	
	all_name_id=all_leader_name_id()


	# if one of the leader can't be found, the page will redirect to the error page
	if not basic0:
		return redirect(url_for('error'))
	if request.args.get('leader1') and not basic2:
		return redirect(url_for('error'))
	return render_template("leaders.html", **locals())	


@app.route("/error")
def error():
	return render_template("error.html")

# direct every other links to the index page
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	return redirect(url_for("index"))

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
		# update config class in development mode
		app.config.from_object('config.DevelopmentConfig')
	else:
		app.config.from_object('config.ProductionConfig')
	
	app.run(threaded=True)






