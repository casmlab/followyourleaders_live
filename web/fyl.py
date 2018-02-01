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


app = Flask('fyl_Umich',static_url_path='/static')

mongo = PyMongo(app)


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/faq")
def faq():
	return render_template("faq.html")

# <legislator> here use ['id']['wikidata']
# @app.route("/legislator_detail/<legislator>", methods=['GET'])
# def leaders_details(legislator):
# 	details = load_legislator_details(legislator)
# 	return render_template("legislator_detail.html", **locals())

@app.route("/leaders")
def leaders():

	user = "H001061" if not request.args.get('leader0') else request.args.get('leader0')
	compare = 'F' if not request.args.get('compare') else request.args.get('compare')
	user2= "H001061" if not request.args.get('leader2') else request.args.get('leader2')


	# Load basic infos	
	basic0 = load_basic_info_fuc(user)
	timeseries_0 = load_timeserie_fuc(user)
	hash_0=load_hash_data(user)
	url_0=load_url_data(user)
	

	if compare=='T':
		basic2 = load_basic_info_fuc(user2)
		timeseries_2 = load_timeserie_fuc(user2)
		hash_2=load_hash_data(user2)
		url_2=load_url_data(user2)
	else:
		basic2={}
		timeseries_2={}
		hash_2={}
		url_2={}

	all_name_id=all_leader_name_id()

	return render_template("leaders.html", **locals())	


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






