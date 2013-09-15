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
			"**Aaand thats all folks!**"
	)
	if words != None:
		return words