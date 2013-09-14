import praw, time, sys, os, json, RTB

config = RTB.loadConfig()

def message(word):
	words = config['words'][word]
	if words != None:
		return words