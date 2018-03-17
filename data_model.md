# Data Model
We store our data in a MongoDB database. Below are descriptions and examples of each collection. The basic process for our data is

1. run purpletag to collect tweets and store then in JSON
2. run script to dump that JSON into ```tweets``` collection
3. run script to parse ```tweets``` collection into the other collections to improve speed of views

## parsing
Here we store info about the parsing that we've done.

```
{
    "_id": ObjectId("23590jlsglk23nlsdf"),
    "last_processed_tweet_id" : NumberLong(697902775301238784),
    "legislators_social_media_yaml_commit" : "09d213213a75fb2083ffbf00c8631f45a6b57667",
    "legislators_current_yaml_commit" : "8c0161d848c8481e69d1343060b9fb988da5497f"
}
```

### Sources
* last_processed_tweet_id get set by the parsing script; also checked by the script when it starts so it knows what data is new

## tweets
The ```tweets``` collection is the heart of the database. Documents here mirror the structure returned by the Twitter API. These documents are *read only*.

```
{
    "_id" : ObjectId("588fc23503fa02a1c221568b"),
    "contributors" : null,
    "truncated" : false,
    "text" : "Glad I could discuss tribal housing issues with the @FallonPaiuteSho &amp; the Walker River Tribe in Schurz today. #NV04 https://t.co/KGvpIAR1zq",
    "is_quote_status" : false,
    "in_reply_to_status_id" : null,
    "id" : NumberLong(697902775301238784),
    "favorite_count" : 1,
    "source" : "<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>",
    "retweeted" : false,
    "coordinates" : null,
    "entities" : {
        "symbols" : [],
        "user_mentions" : [],
        "hashtags" : [ 
            {
                "indices" : [ 
                    115, 
                    120
                ],
                "text" : "NV04"
            }
        ],
        "urls" : [],
        "media" : [ 
            {
                "expanded_url" : "http://twitter.com/RepHardy/status/697902775301238784/photo/1",
                "display_url" : "pic.twitter.com/KGvpIAR1zq",
                "url" : "https://t.co/KGvpIAR1zq",
                "media_url_https" : "https://pbs.twimg.com/media/Ca9y4DhWwAA8ShG.jpg",
                "id_str" : "697902774609166336",
                "sizes" : {
                    "large" : {
                        "h" : 680,
                        "resize" : "fit",
                        "w" : 1024
                    },
                    "small" : {
                        "h" : 226,
                        "resize" : "fit",
                        "w" : 340
                    },
                    "medium" : {
                        "h" : 399,
                        "resize" : "fit",
                        "w" : 600
                    },
                    "thumb" : {
                        "h" : 150,
                        "resize" : "crop",
                        "w" : 150
                    }
                },
                "indices" : [ 
                    121, 
                    144
                ],
                "type" : "photo",
                "id" : NumberLong(697902774609166336),
                "media_url" : "http://pbs.twimg.com/media/Ca9y4DhWwAA8ShG.jpg"
            }
        ]
    },
    "in_reply_to_screen_name" : null,
    "id_str" : "697902775301238784",
    "retweet_count" : 3,
    "in_reply_to_user_id" : null,
    "favorited" : false,
    "user" : {
        "follow_request_sent" : false,
        "has_extended_profile" : false,
        "profile_use_background_image" : true,
        "default_profile_image" : false,
        "id" : NumberLong(2964222544),
        "profile_background_image_url_https" : "https://abs.twimg.com/images/themes/theme1/bg.png",
        "verified" : true,
        "profile_text_color" : "333333",
        "profile_image_url_https" : "https://pbs.twimg.com/profile_images/552515282728521729/bazgL2JV_normal.jpeg",
        "profile_sidebar_fill_color" : "DDEEF6",
        "entities" : {
            "url" : {
                "urls" : [ 
                    {
                        "url" : "http://t.co/RPDLpARNAe",
                        "indices" : [ 
                            0, 
                            22
                        ],
                        "expanded_url" : "http://hardy.house.gov",
                        "display_url" : "hardy.house.gov"
                    }
                ]
            },
            "description" : {
                "urls" : []
            }
        },
        "followers_count" : 1920,
        "profile_sidebar_border_color" : "C0DEED",
        "id_str" : "2964222544",
        "profile_background_color" : "C0DEED",
        "listed_count" : 129,
        "is_translation_enabled" : true,
        "utc_offset" : -18000,
        "statuses_count" : 793,
        "description" : "Proudly representing Nevada's 4th Congressional District",
        "friends_count" : 392,
        "location" : "Nevada, USA",
        "profile_link_color" : "0084B4",
        "profile_image_url" : "http://pbs.twimg.com/profile_images/552515282728521729/bazgL2JV_normal.jpeg",
        "following" : false,
        "geo_enabled" : true,
        "profile_banner_url" : "https://pbs.twimg.com/profile_banners/2964222544/1446734903",
        "profile_background_image_url" : "http://abs.twimg.com/images/themes/theme1/bg.png",
        "screen_name" : "RepHardy",
        "lang" : "en",
        "profile_background_tile" : false,
        "favourites_count" : 97,
        "name" : "Rep. Cresent Hardy",
        "notifications" : false,
        "url" : "http://t.co/RPDLpARNAe",
        "created_at" : "Tue Jan 06 14:08:31 +0000 2015",
        "contributors_enabled" : false,
        "time_zone" : "Eastern Time (US & Canada)",
        "protected" : false,
        "default_profile" : true,
        "is_translator" : false
    },
    "geo" : null,
    "in_reply_to_user_id_str" : null,
    "possibly_sensitive" : false,
    "lang" : "en",
    "created_at" : "Thu Feb 11 21:59:22 +0000 2016",
    "in_reply_to_status_id_str" : null,
    "place" : null,
    "extended_entities" : {
        "media" : [ 
            {
                "expanded_url" : "http://twitter.com/RepHardy/status/697902775301238784/photo/1",
                "display_url" : "pic.twitter.com/KGvpIAR1zq",
                "url" : "https://t.co/KGvpIAR1zq",
                "media_url_https" : "https://pbs.twimg.com/media/Ca9y4DhWwAA8ShG.jpg",
                "id_str" : "697902774609166336",
                "sizes" : {
                    "large" : {
                        "h" : 680,
                        "resize" : "fit",
                        "w" : 1024
                    },
                    "small" : {
                        "h" : 226,
                        "resize" : "fit",
                        "w" : 340
                    },
                    "medium" : {
                        "h" : 399,
                        "resize" : "fit",
                        "w" : 600
                    },
                    "thumb" : {
                        "h" : 150,
                        "resize" : "crop",
                        "w" : 150
                    }
                },
                "indices" : [ 
                    121, 
                    144
                ],
                "type" : "photo",
                "id" : NumberLong(697902774609166336),
                "media_url" : "http://pbs.twimg.com/media/Ca9y4DhWwAA8ShG.jpg"
            }
        ]
    }
}
```

### Sources
* .json files produced by purpletag queries

## yaml

### Sources
* [https://github.com/unitedstates/congress-legislators/blob/master/legislators-social-media.yaml](https://github.com/unitedstates/congress-legislators/blob/master/legislators-social-media.yaml)
* [https://github.com/unitedstates/congress-legislators/blob/master/legislators-current.yaml](https://github.com/unitedstates/congress-legislators/blob/master/legislators-current.yaml)

## leaders
This collection contains information about the leaders. For members of the U.S. Congress, this data comes from [the unitedstates project](https://github.com/unitedstates/congress-legislators), which we store in the ```yaml``` collection and then parse here for speed and to add Twitter info.

```
{
    "_id" : ObjectId("58f67c3099fec16d7678ec5a"),
    "bioguide" : "R000600",
    "description" : "Congresswoman Representing American Samoa",
    "birthday" : "1947-12-29",
    "wikidata" : "Q18684027",
    "name" : "Aumua Amata Coleman Radewagen",
    "gender" : "F",
    "religion" : "Unknown",
    "state" : "AS",
    "twitter_name" : "RepAmata",
    "twitter_id" : 3026622545,
    "party" : "Republican",
    "chamber" : "house",
    "photo_url" : "https://pbs.twimg.com/profile_images/552515282728521729/bazgL2JV_normal.jpeg",
    "followers" : 120,
    "friends" : 5,
    "recent_tweet_ids" : [],
    "current" : 1
}
```

### Sources
* last tweet: photo_url, followers, friends, recent_tweet_ids
* yaml: the rest 

## timelines
This collection supports the timeline views and organizes tweets by date and person.

```
{
    "_id" : ObjectId("58e6828e99fec16ab94ee0fa"),
    "bioguide" : "R000600"
    "twitter_id" : 3026622545,
    "twitter_name" : "RepAmata",
    "dates" : {
        "2015-02-09" : {
            "564820451508383746" : {
                "url" : "https://twitter.com/RepAmata/status/564820451508383746",
                "created_at" : "2015-02-09 16:17:44",
                "hashtags" : [ "fomo" ],
                "tweet_text" : "here's what the tweet said"
            },
            "564820451508383746" : {
                "url" : "https://twitter.com/RepAmata/status/564820451508383746",
                "created_at" : "2015-02-09 16:17:44",
                "hashtags" : [ "repamata", "tcot" ],
                "tweet_text" : "here's what the tweet said"
            }
        }
        "2015-02-10" : {
            "564820451508383746" : {
                "url" : "https://twitter.com/RepAmata/status/564820451508383746",
                "created_at" : "2015-02-09 16:17:44",
                "hashtags" : [ "fomo" ],
                "tweet_text" : "here's what the tweet said"
            }
        }
    }
}
```

## hashtags
This collection supports the hashtag clouds. It organizes hashtags by person and allows us to restrict tags and tweets by date.

```
{
    "_id" : ObjectId("58e6828e99fec16ab94ee0fa"),
    "bioguide" : "F000448",
    "hashtags": {
        "emp" : {
            "tweets" : {
                "923900301895262209" : {
                    "created_at" : "2015-02-09 16:17:44",
                    "tweet_text" : "here's my tweet text #emp"
                },
                "923900301895262210" : {
                    "created_at" : "2015-02-09 16:17:50",
                    "tweet_text" : "here's my 2nd tweet text #emp"
                }
            }
        }
    }
}
```

### Sources:
* tweets collection

## urls
This collection supports the URL views. It works like the ```hashtags``` collection.

```
{
    "_id" : ObjectId("58e6828e99fec16ab94ee0fa"),
    "bioguide" : "F000448",
    "urls": {
        "http://bit\u002ely/TonkoGrid" : {
            "tweets" : {
                "923900301895262209" : {
                    "created_at" : "2015-02-09 16:17:44",
                    "tweet_text" : "here's my tweet text http://bit.ly/TonkoGrid"
                },
                "923900301895262210" : {
                    "created_at" : "2015-02-09 16:17:50",
                    "tweet_text" : "here's my 2nd tweet text http://bit.ly/TonkoGrid"
                }
            }
        }
    }
}
```

### Sources
* tweets collection