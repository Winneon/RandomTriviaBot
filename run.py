import praw, time, sys, os, json

defaultConfig = {
    'reddit': {
        'username': '',
        'password': '',
        'alert': '',
		},
}

def writeConfig(conf):
	config = json.dumps(conf, indent = 4, sort_keys = True)
	with open('config.json', 'w') as f:
		f.write(config)


if __name__ == "__main__":
	if not os.path.isfile('config.json'):
		writeConfig(defaultConfig)
		print("[ wsRTB ] - Created default configuration. Please edit the values before you start this again.")
	elif 'updateconf' in sys.argv:
		with open('config.json', 'r') as f:
			config = json.loads(f.read())
		defaultConfig.update(config)
		writeConfig(defaultConfig)
	else:
		import RTB
		RTB.main()
