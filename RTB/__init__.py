import praw, time, sys, os, json
from RTB.messages import message

def loadConfig():
	config = json.loads(open('config.json').read())
	return config

config = loadConfig()

def handleRateLimit(func, *args):
	while True:
		try:
			func(*args)
			break
		except praw.errors.RateLimitExceeded as error:
			print("\tRate limit exceeded! Sleeping for %d seconds" % error.sleep_time)
			time.sleep(error.sleep_time)

def main():
	version = "v1.1"
	
	bannedSubs = set()
	bannedSubs.add('gonewild')
	bannedSubs.add('GoneWildPlus')
	bannedSubs.add('porn')
	bannedSubs.add('nsfw')
	
	userAgent = (
		"/u/WinneonSword's beloved RandomTriviaBot, " + version +
		"For more: http://github.com/WinneonSword/RandomTriviaBot ( Coming soon! )"
	)
	
	r = praw.Reddit(user_agent = userAgent)
	
	username = config['reddit']['username']
	password = config['reddit']['password']
    
	r.login(username, password)
	
	userAlert = config['reddit']['alert']
	subjectAlert = "RandomTriviaBot has been activated"
	messageAlert = (
					"**Hello there,**" + "\n\n"
					"This is **RandomTriviaBot**. As you can see with this message, I have been activated, so if I have not been activated by you, then please turn me off." + "\n\n"
					"**Thanks,**" + "\n\n"
					"RandomTriviaBot, " + version
    )
	
	r.send_message(userAlert, subjectAlert, messageAlert)
	cache = []
	
	activationWords = ['cactus', 'rofl', 'banana', 'wine', 'tomato']
	while True:
		print("[ wsRTB ] - Fetching new posts...")
		subreddit = r.get_subreddit("all")
		for submission in subreddit.get_new(limit = 30):
			selfPost = submission.selftext.lower()
			selfTitle = submission.title.lower()
			hasWord = any(string in selfPost for string in activationWords)
			hasTitle = any(string in selfTitle for string in activationWords)
			if submission.id not in cache and hasWord:
				if submission.subreddit.display_name not in bannedSubs:
					temp = [(selfPost.find(i), i) for i in activationWords if i in selfPost]
					word = min(temp)[1]
					print("\tFound valid post at submission id '" + submission.id + "'! Adding comment...")
					handleRateLimit(submission.add_comment, message(word))
					cache.append(submission.id)
					print("\tComment posted!")
					break
				else:
					print("\tThe subreddit '" + submission.subreddit + "' is in the bannedSubs list!")
					break
			if submission.id not in cache and hasTitle:
				if submission.subreddit.display_name not in bannedSubs:
					print("\tFound valid post at submission id of '" + submission.id + "'! Adding comment...")
					temp = [(selfTitle.find(i), i) for i in activationWords if i in selfTitle]
					word = min(temp)[1]
					handleRateLimit(submission.add_comment, message(word))
					cache.append(submission.id)
					print("\tComment posted!")
					break
				else:
					print("\tThe subreddit '" + submission.subreddit + "' is in the bannedSubs list!")
					break
		time.sleep(30)