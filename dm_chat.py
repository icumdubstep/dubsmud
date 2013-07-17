#
# dm_chat.py - Python file that handles chat n' stuff
#

# Imports
import dm_global

class ChatChannel: # Class for a specific channel for the chat.
	def __init__(self, close_on_vacant=False, name="System", private=False):
		self.name = name
		self.readonly = False
		self.topic = "Topic not set"
		self.connected_players = []
		self.close_on_vacant = close_on_vacant
		self.chat_color = ""
		self.private = private
	def broadcast(self, msg):
		for player in self.connected_players:
			if player.ansi_color_enabled:
				player.send_message("{0}{1} > {2}{3}".format(self.chat_color, self.name, msg, dm_global.CLEAR_FORMATTING))
			else:
				player.send_message("{0} > {1}".format((self.name, msg)))
	def add_player(self, player):
		if player in self.connected_players:
			player.send_message("Already connected to that channel")
		else:
			self.broadcast("%s connected to %s" % (player.name, self.name) )
			self.connected_players.append(player)
			player.send_message("Connected to {0}".format(self.name))
	#Removes a player from the list. If the close_on_vacant flag is True, and the channel is vacant, the channel will return True. ChatManager will then close the channel
	def remove_player(self, player):
		if player in self.connected_players:
			self.connected_players.remove(player)
			self.broadcast("%s disconnected from %s" % (player.name, self.name) )
			player.send_message("Disconnected from {0}".format(self.name))
			if self.close_on_vacant and not self.connected_players:
				return True
		else:
			player.send_message("Not connected to {0}".format(self.name))
		return False
	def change_topic(self, player, topic):
		if player in self.connected_players:
			self.topic = topic
			self.broadcast("{0} has changed the topic to {1}".format(player.name, topic))
		else:
			player.send_message("Not connected to {0}".format(self.name))