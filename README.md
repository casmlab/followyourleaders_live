# New Follow Your Leaders code

Follow Your Leaders is part of a larger research project about politicians and social media from the Collaboration and Social Media Lab at the Illinois Institute of Technology. The goal of the website is to allow users to explore data from Twitter and other sources to see how politicians use social media. You can read more about our research at the CaSM Lab website. 

## Overview

### Code Structure
```
./fyl_2017
  __init__.py
  fyl.py
  data_load.py
  static
    css
      compare.css
  templates
    base.html
    compare_default.html
    compare_result.html
    faq.html
    index.html
    legislators.html
    legislator_detail.html
  etl
    fyl_etl.py
    stop_words.txt
```

### Technology Stack

[Bootstrap](http://getbootstrap.com/) + [Flask](http://flask.pocoo.org/) + [MongoDB](https://www.mongodb.com/) + [Google Charts](https://developers.google.com/chart/)


## Development

* ssh forward to localhost 5000 port
```
ssh -L 5000:esposito.casmlab.org:5000 [username]@esposito.casmlab.org
```

* Use virtualenv
```
bin/virtualenv fyl
. fyl/bin/activate
```

* Meet all the requirements
```
pip install -r requirements.txt
```

* Run fyl.py with development mode
```
fyl.py -m dev
```

* Check browser on address 'localhost:5000'


## Data Model

The data that support follow_your_leader website is structured in MongoDB. It was originally converted from `1455333733.json`, and the most up-to-date tweets are expected to be added. Inside the `fyl` db, there are totally 5 collections, `tweets` collection contains all the origin data converted from `1455333733.json`, `users` collection supports `legislator_detail.html`, `timelines` & `word_freq` & `sentiment` provide data to google charts to create related graphs for legislators comparisons.

### tweets document
```
{
  "_id" : ObjectId("588fc23403fa02a1c221568a"),
  "contributors" : null,
	"truncated" : false,
	"text" : "Hello everyone, I'm excited to join Twitter to share the work I'm doing in Congress on behalf of the American Samoan people.",
	"in_reply_to_screen_name" : null,
	"id_str" : "564820451508383746",
	"retweet_count" : 15,
	"in_reply_to_user_id" : null,
	"favorited" : false,
	"user" : {
    ...
  }
  ...
}
```

### users document
```
{
  "_id": ObjectId("5899fa9a99fec10c2a3d2c80"),
  "bioguide" : "R000600",
  "description" : "Congresswoman Representing American Samoa",
  "birthday" : "1947-12-29",
  "wikidata" : "Q18684027",
  "name" : "Aumua Amata Coleman Radewagen",
  "gender" : "F",
  "religion" : "Unknown",
  "state" : "AS",
  "twitter_name" : "RepAmata",
  "party" : "Republican",
  "type" : "house",
  "recent_tweets" : [{...}, {...}, ...]
}
```

### timelines document
```
{
  "_id": ObjectId("58a1378499fec11027d61cb6"),
  "name" : "RepBThompson",
  "time_counts" : { 
    "Feb 04 2016" : 1,
    "Sep 12 2014" : 2
  }
} 
```

### word_freq document
```
{
  "_id": ObjectId("58a1378499fec11027d61cb6"),
  "name" : "RepBThompson",
  "word_freq": {
    "toured" : 4,
    "percent" : 15,
    "ranks" : 3,
    "Shooting" : 2
  }
}
```

### sentiment document
```
{
  "_id" : ObjectId("58d05e6d99fec12f5ce1765a"),
  "name" : "Ken Calvert",
  "Other" : 3843,
  "Narrative" : 695,
  "Provinfo" : 228,
  "Position" : 7281,
  "Reqaction" : 449,
  "Thanks" : 0
}
```

## Data Cleaning & Transformation

The tweets data stored in `tweets` need to be cleaned & transformed to support various charts. The Python scripts reside in `./etl`. Data in `tweets` will be transformed into different formats and stored in corresponding collections.

## Resources
* [Members of the United States Congress, 1789-Present, in YAML, as well as committees, presidents, and vice presidents](https://github.com/unitedstates/congress-legislators)


