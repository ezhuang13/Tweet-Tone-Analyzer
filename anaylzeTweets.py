# analyzeTweets

from twitterSearch import findTweets
from watsonAnalyze import analyze
import plotly, sys
import plotly.graph_objs as go
from plotly.graph_objs import Layout

# Command line argument 1: hashtag to search
# (Optional) arg 2: 'e' or 's' to search emotional or social data
# (Optional) arg 3: 'b' or 'p' to display in bar graph or pie chart

# Checks to ensure there is a command line argument for hashtag
if len(sys.argv) > 1:
    hashtag = sys.argv[1]
else:
    print ('Error! Command line argument required')
    sys.exit()

# Inserts hashtag if it is not already there
if hashtag[0] != '#':
	hashtag = '#' + hashtag
print('Scanning through tweets containing ' + hashtag)
tweets = findTweets(hashtag)

# Analyzes tweets and assigns aggregate scores for each possible tone
scores = analyze(tweets)
emotionalScore = scores[0]
socialScore = scores[1]

# Colors for bar graphs
colors = ['rgba(224,26,26, 1)', 'rgba(43, 26, 224, 1)',
               'rgba(26, 224, 33, 1)', 'rgba(224, 178, 26, 1)',
               'rgba(148, 26, 224, 1)']

if len(sys.argv) != 4:
	# Allows user to choose type of data
	print('Would you like emotional data (e) or social data (s)?')
	dataType = input()
	while dataType != 'e' and dataType != 's':
		print('Not a valid command! Please choose "e" or "s"')
		dataType = input()

	# Allows user to choose presentation style of data
	print('Would you like a pie chart (p) or bar graph (b)?')
	graphType = input()
	while graphType != 'b' and graphType != 'p':
		print('Not a valid command! Please choose "p" or "b"')
		graphType = input()
else:
	dataType = sys.argv[2]
	graphType = sys.argv[3]

# Creates and displays graphs
if dataType == 'e':
	if graphType == 'b':
		emotionData = [go.Bar(x = list(emotionalScore.keys()), y = list(emotionalScore.values()),
		marker=dict(color=colors))]
	else:
		emotionData = [go.Pie(labels = list(emotionalScore.keys()), values = list(emotionalScore.values()))]
	plotly.offline.plot({'data': emotionData, 'layout': Layout(title='Emotional tones for ' + hashtag)})
else:
	if graphType == 'b':
		socialData = [go.Bar(x = list(socialScore.keys()), y = list(socialScore.values()),
		marker=dict(color=colors))]
	else:
		socialData = [go.Pie(labels = list(socialScore.keys()), values = list(socialScore.values()))]
	plotly.offline.plot({'data': socialData, 'layout': Layout(title='Social tones for ' + hashtag)})
