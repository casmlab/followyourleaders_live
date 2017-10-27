import tweepy  
consumer_key = "znlVBxsyl3vfC6zw4GV2FrzJ1"  
consumer_secret = "iV3KxtERw2r2Gql2Sd5IhdIA8tisx8sjmiAqUbYfKvKfSeSpXf"  
access_token = "770104672388612100-fFsQsXQV2m4DoFtJ6PLywjzVHkirEy6"  
access_token_secret = "G3ZhpfmxgxWj07XUw5oKu8TQNkJW872gstVtMShdSqdpf"  

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  
api = tweepy.API(auth)  



name = "nytimes"  
tweetCount = 20

results = api.user_timeline(id=name, count=tweetCount)

for tweet in results:  
   print tweet.text


   #http://www.itran.cc/2017/06/15/twitter-data-mining-using-python/