import praw, time, sys, os, json

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
	cactusMessage = (
					"**Hello,**" + "\n\n"
					"The word *cactus* was found in your post!" + "\n\n"
					"Did you know that the word *cactus* has 3 different plural variations? (cacti, cactuses, or cactus)" + "\n\n"
					"**Aaand thats all folks!**"
	)
	
	activationWords = ['cactus', 'cacti']
	while True:
		print("[ wsRTB ] - Fetching new posts...")
		subreddit = r.get_subreddit("all")
		for submission in subreddit.get_new(limit = 30):
			selfPost = submission.selftext.lower()
			selfTitle = submission.title.lower()
			hasWord = any(string in selfPost for string in activationWords)
			hasTitle = any(string in selfTitle for string in activationWords)
			if submission.id not in cache and hasWord:
				print("\tFound valid post at submission id '" + submission.id + "'! Adding comment...")
				handleRateLimit(submission.add_comment, cactusMessage)
				cache.append(submission.id)
				print("\tComment posted!")
				break
			if submission.id not in cache and hasTitle:
				print("\tFound valid post at submission id of '" + submission.id + "'! Adding comment...")
				handleRateLimit(submission.add_comment, cactusMessage)
				cache.append(submission.id)
				print("\tComment posted!")
				break
		time.sleep(30)