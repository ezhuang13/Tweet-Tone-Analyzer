# twitterSearch.py 

from twitter import OAuth, Twitter
import json
import re

# Variables needed to access Twitter API
CONSUMER_KEY = '8yXCHyxT8m4XrWa2AdEdGEFJm'
ACCESS_TOKEN = '832367041109749760-45fF5jnpGJ6X34f0JcHujH9QVaShfiG'
# TODO: Make these non-human-readable
CONSUMER_SECRET = 'oiwWFmU1Nmlfh5DWCU5XJ30SA3N9OcHaRDC06tma5qfb3Qx3Qw'
ACCESS_SECRET = 'WCsOmFvUzBEfnbKdleEKlhzmj3TJw16TOLRljd6WNWBms'

# Authentification and creation of Twitter object
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
t = Twitter(auth=oauth)

# Creation of regex to keep only specified characters
alphaPunct = re.compile("[^a-zA-Z!.,?#'@ ]")

def findTweets(hashtag):
	# Makes query and stores result in results
	results = t.search.tweets(q=hashtag, result_type='recent', lang='en', count=200)
	# Remove metadata aspect of tweets. We aren't the NSA so we don't need it
	results = results['statuses']

	# Displays some example tweets for the user
	tweetEx = []
	limit = 3
	for tweet in results:
		if limit == 0:
			break
		tweetEx.append(json.dumps(tweet['text']))
		limit -= 1
	print('Analyzing tweets such as:')
	for tweet in tweetEx:
		tweet = processTweet(tweet)
		print(tweet)

	# Stores and processes tweets
	tweets = ''
	for tweet in results:
		s = json.dumps(tweet['text'])
		s = processTweet(s)
		tweets += s
	return tweets

# Removes excess characters from tweets
def processTweet(tweet):
	# Remove clutter from any retweets
	if len(tweet) > 3 and (tweet[1] + tweet[2]) == 'RT':
		start = 0
		for c in tweet:
			if c != ':':
				start += 1
			else:
				tweet = tweet[start + 2:]
				break

	# Removes any links in tweets
	tweet = re.split(' |\\n', tweet)
	indicesToRemove = []
	for index in range(len(tweet)):
		word = tweet[index]
		if 'https' in word or '\\u' in word: # Note: \u is emoji removal
			indicesToRemove.append(index)
	numRemoved = 0
	for index in indicesToRemove:
		tweet.pop(index - numRemoved)
		numRemoved += 1
	tweet = ' '.join(tweet)

	# Removes any characters not in alphaPunct
	tweet = alphaPunct.sub('', tweet)
	return tweet
