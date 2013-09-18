import praw, time, sys, os, json
from RTB.messages import message
from warnings import filterwarnings

filterwarnings("ignore", category = DeprecationWarning)
filterwarnings("ignore", category = ResourceWarning)

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
			print("\tRate Limit exceeded! Sleeping for %d seconds to comply with the Reddit API..." % error.sleep_time)
			time.sleep(error.sleep_time)

def main():
	version = "v1.1"
	
	bannedSubs = set()
	bannedSubs.add('gonewild')
	bannedSubs.add('GoneWildPlus')
	bannedSubs.add('porn')
	bannedSubs.add('nsfw')
	bannedSubs.add('NetherWreck')
	bannedSubs.add('magicTCG')
	bannedSubs.add('sanfrancisco')
	bannedSubs.add('gardening')
	bannedSubs.add('ibs')
	bannedSubs.add('pokemonzetaomicron')
	bannedSubs.add('learnpython')
	bannedSubs.add('wine')
	bannedSubs.add('CivCarson')
	bannedSubs.add('malefashionadvice')
	bannedSubs.add('Android')
	bannedSubs.add('seduction')
	bannedSubs.add('miamidolphins')
	bannedSubs.add('slowcooking')
	
	userAgent = (
		"/u/WinneonSword's beloved RandomTriviaBot, " + version +
		"For more: http://github.com/WinneonSword/RandomTriviaBot"
	)
	
	username = config['reddit']['username']
	password = config['reddit']['password']
	print("[ wsRTB ] - Attempting to connect & login to Reddit...")
	try:
		r = praw.Reddit(user_agent = userAgent)
		r.login(username, password)
		print("\tSuccessfully connected & logged in to Reddit!")
	except:
		print("\tCould not connect to Reddit. Check reddit.com or your config for errors.")
		sys.exit()
	
	cache = []
	
	activationWords = [' cactus ', ' rofl ', ' banana ', ' wine ', ' tomato ', ' pineapple ', ' dolphin ']
	try:
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
						print("\tThe subreddit '" + submission.subreddit.display_name + "' is in the bannedSubs list!")
						break
				if submission.id not in cache and hasTitle:
					if submission.subreddit.display_name not in bannedSubs:
						print("\tFound valid post at submission id '" + submission.id + "'! Adding comment...")
						temp = [(selfTitle.find(i), i) for i in activationWords if i in selfTitle]
						word = min(temp)[1]
						handleRateLimit(submission.add_comment, message(word))
						cache.append(submission.id)
						print("\tComment posted!")
						break
					else:
						print("\tThe subreddit '" + submission.subreddit.display_name + "' is in the bannedSubs list!")
						break
			time.sleep(30)
	except KeyboardInterrupt:
		print("[ wsRTB ] - Stopped RandomTriviaBot!")		