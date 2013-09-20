import praw, time, sys, os, json, argparse

# The default configuration that the login and alert scripts read.
defaultConfig = {
	'reddit': {
		'username': '',
		'password': '',
		},
	'words': {
		'cactus': 'Did you know that the word *cactus* has 3 different plural variations? (cacti, cactuses, or cactus)',
		'rofl': 'Did you know that on March 24th, 2011, the acronym *rofl* was added to the Oxford English Dictionary?',
		'banana': 'Did you know that there is a book called "Fighting the Banana Wars and other Fairtrade Battles" by Harriet Lamb?',
		'wine': 'Did you know that *wine* has been in production dating back to 7000 BC?',
		'tomato': 'Did you know that *tomatoes* can be considered as a fruit AND a vegetable?',
		'pineapple': 'Did you know that if you eat a lot of *pineapple*, your taste buds will taste things sweeter than normal?',
		'dolphin': 'Did you know that dolphins swim in groups up to several hundred in size?'
		},
}

def writeConfig(conf):
	config = json.dumps(conf, indent = 4, sort_keys = True)
	with open('config.json', 'w') as f:
		f.write(config)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'RandomTriviaBot')
	parser.add_argument('-l', '--login', action = 'store_true', help = 'Login to a different account')
	args = parser.parse_args()
	if not os.path.isfile('config.json'):
		writeConfig(defaultConfig)
		print("[ wsRTB ] - Created default configuration. Please edit the values before you start this again.")
	elif 'updateconf' in sys.argv:
		with open('config.json', 'r') as f:
			config = json.loads(f.read())
		defaultConfig.update(config)
		writeConfig(defaultConfig)
	else:
		if args.login:
			import RTB
			RTB.customLogin()
		else:
			import RTB
			RTB.login()