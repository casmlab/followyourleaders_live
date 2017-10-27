#https://stackoverflow.com/questions/13975021/merge-join-lists-of-dictionaries-based-on-a-common-value-in-python
import pymongo
import urllib
import yaml
from collections import defaultdict
import itertools 





# combine two yamls file by 'bioguide'
legislators_file = urllib.urlopen('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml')
list_a = yaml.load(legislators_file)

media = urllib.urlopen('https://theunitedstates.io/congress-legislators/legislators-social-media.yaml')
list_b = yaml.load(media)


lst = sorted(itertools.chain(list_a,list_b), key=lambda x:x['id']['bioguide'])
list_c = []
for k,v in itertools.groupby(lst, key=lambda x:x['id']['bioguide']):
    d = {}
    for dct in v:
        d.update(dct)
    list_c.append(d)


#creating new collection
client = pymongo.MongoClient()
db = client['fyl']
collect = db['yaml']
for i in list_c:
    collect.insert(i)

