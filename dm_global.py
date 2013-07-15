#
# dm_global.py - The file that stores any data that is global to the dubsmud application
#

# Imports
import dm_chat

#Color dictionary

COLORS = {
		"n_black": "\x1b[30m",
		"n_red": "\x1b[31m",
		"n_green": "\x1b[32m",
		"n_yellow": "\x1b[33m",
		"n_blue": "\x1b[34m",
		"n_magenta": "\x1b[35m",
		"n_cyan": "\x1b[36m",
		"n_white": "\x1b[37m",
		"b_black": "\x1b[30;1m",
		"b_red": "\x1b[31;1m",
		"b_green": "\x1b[32;1m",
		"b_yellow": "\x1b[33;1m",
		"b_blue": "\x1b[34;1m",
		"b_magenta": "\x1b[35;1m",
		"b_cyan": "\x1b[36;1m",
		"b_white": "\x1b[37;1m",
		"bn_black": "\x1b[30m",
		"bn_red": "\x1b[41m",
		"bn_green": "\x1b[42m",
		"bn_yellow": "\x1b[43m",
		"bn_blue": "\x1b[44m",
		"bn_magenta": "\x1b[45m",
		"bn_cyan": "\x1b[46m",
		"bn_white": "\x1b[47m",
		"bb_black": "\x1b[40;1m",
		"bb_red": "\x1b[41;1m",
		"bb_green": "\x1b[42;1m",
		"bb_yellow": "\x1b[43;1m",
		"bb_blue": "\x1b[44;1m",
		"bb_magenta": "\x1b[45;1m",
		"bb_cyan": "\x1b[46;1m",
		"bb_white": "\x1b[47;1m"
}
CLEAR_FORMATTING = "\x1b[0m"
# List of all connecting players
PLAYER_LIST = []
# The managing object for all chat.
CHAT_MANAGER = dm_chat.ChatManager()
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