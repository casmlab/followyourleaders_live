import pymongo
import urllib
import yaml

# creating new collection
# client = pymongo.MongoClient()
# db = client['fyl']
# collect = db['yaml']
# legislators_file = urllib.urlopen('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml')
# legislators_obj = yaml.load(legislators_file)	
# for i in legislators_obj:
# 	 collect.insert(i)




# client = pymongo.MongoClient()
# db = client['fyl']
# collect = db['yaml']

# print collect.find_one({"name.official_full":"Joaquin Castro"})




legislators_file = urllib.urlopen('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml')
legislators_obj = yaml.load(legislators_file)

media = urllib.urlopen('https://theunitedstates.io/congress-legislators/legislators-social-media.yaml')
media_obj = yaml.load(media)