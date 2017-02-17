# watsonAnalyze.py 

from watson_developer_cloud import ToneAnalyzerV3
import json

# Given a block of text, analyzes data and returns a tuple
# of dictionaries containing emotional and social tone data
def analyze(text):
	user = '09acf38c-1d4b-42a0-91e9-be8b17a726df'
	passcode = 'etDAyCcoXGxY'

	toneAnalyzer = ToneAnalyzerV3(username=user, password=passcode, version='2016-02-11')

	# Processes tones given by tone analyzer
	tones = toneAnalyzer.tone(text=text)
	tones = tones['document_tone']['tone_categories']
	emotions = tones[0]['tones']
	social = tones[2]['tones']
	emotionTones = {}
	socialTones = {}

	# Assigns a score for each type of tone
	for tone in emotions:
		emotionTones[tone['tone_name']] = tone['score']
	for tone in social:
		socialTones[tone['tone_name']] = tone['score']

	return(emotionTones, socialTones)
