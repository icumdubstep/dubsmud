#
# dm_global.py - The file that stores any data that is global to the dubsmud application
#

# Imports
import dm_chat

#Color dictionary

COLORS = {
		"black": "\x1b[30m",
		"red": "\x1b[31m",
		"green": "\x1b[32m",
		"yellow": "\x1b[33m",
		"blue": "\x1b[34m",
		"magenta": "\x1b[35m",
		"cyan": "\x1b[36m",
		"white": "\x1b[37m",
		"b_black": "\x1b[30m",
		"b_red": "\x1b[41m",
		"b_green": "\x1b[42m",
		"b_yellow": "\x1b[43m",
		"b_blue": "\x1b[44m",
		"b_magenta": "\x1b[45m",
		"b_cyan": "\x1b[46m",
		"b_white": "\x1b[47m",
}
CHAT_CHANNELS = {"System": dm_chat.ChatChannel(False), "default": dm_chat.ChatChannel(False, "default")}
CHAT_CHANNELS["System"].readonly = True
CLEAR_FORMATTING = "\x1b[0m"
# List of all connecting players
PLAYER_LIST = []
# The managing object for all chat.

# Run condition for server loop
SERVER_RUN = True

RULES = ""
# global functions

def broadcast(msg):
	"""
	Send msg to every client.
	"""
	for player in PLAYER_LIST:
		player.client.send(msg)
		player.client.send("\n")