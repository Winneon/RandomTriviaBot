import praw, time, sys, os, json

def loadConfig():
	config = json.loads(open('config.json').read())
	return config

config = loadConfig()

def message(word):
	words = (
			"**Hello,**" + "\n\n"
			"The word *" + word +"* was found in your post!" + "\n\n"
			"" + config['words'][word] + "\n\n"
			"**Aaand thats all folks!**" + "\n\n"
			"*****" + "\n\n"
			"^This ^bot ^is ^not ^meant ^as ^an ^annoyance ^or ^distraction. ^If ^it ^is, ^then ^feel ^free ^to ^contact ^/u/WinneonSword ^or ^post ^at ^/r/RandomTriviaBot ^and ^the ^subreddit ^will ^be ^added ^to ^RandomTriviaBot's ^filters."
	)
	if words != None:
		return words