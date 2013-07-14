#
# dm_chat.py - Python file that handles chat n' stuff
#

# Imports
import dm_global

class ChatChannel: # Class for a specific channel for the chat.
	def __init__(self, close_on_vacant=True, name="System"):
		self.name = name
		self.color = "\x1b[31;1m"
		self.readonly = False
		self.topic = "Topic not set"
		self.connected_players = []
		self.close_on_vacant = close_on_vacant
	def broadcast(self, msg):
		for player in self.connected_players:
			player.send_message("%s > %s" % (self.get_display_name(), msg))
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
	def get_display_name(self):
		return self.color + self.name + "\x1b[37;1m"
class ChatManager:
	def __init__(self):
		self.channels = {'System': ChatChannel(False), 'default': ChatChannel(False, "default")}
		self.channels['System'].readonly = True
	def add_channel(self, channel_name):
		if ' ' in channel_name:
			return "Channel name invalid"
		elif channel_name in self.channels:
			return "Channel already open"
		else:
			self.channels[channel_name] = ChatChannel( True, channel_name )
	#This is different from handle_message in that it a) changes the channel topic and b) takes the whole command as input for msg
	def display_topic(self, player, channel):
		try:
			player.send_message("Topic for {0}: {1}".format((channel, self.channels[channel].topic)))
		except KeyError as e:
			player.send_message("Channel {0} not found".format(target_channel))
	def change_topic(self, player, channel, topic):
		if channel in self.channels:
			self.channels[channel].topic = topic
			self.channels[channel].broadcast("*%s has changed the topic to \"%s\"" % (player.name, msg[msg.index(' ') + 1:]))
			player.last_channel = channel
		else:
			player.send_message("Channel {0} not found".format(target_channel))
	def handle_message(self, msg, player, target_channels=[], me=False):
		for channel in target_channels:
			if channel in self.channels:
				if self.channels[channel].readonly and not player.admin:
					player.send_message("You are not allowed to send messages to this channel.")
				else: 
					if me:
						self.channels[channel].broadcast("*%s %s" % (player.name, msg))
					else:
						self.channels[channel].broadcast("%s : %s" % (player.name, msg))
					player.last_channel = channel
			else:
				return "Channel {0} not found".format(channel)
	def add_player_to_channel(self, player, channel="System"):
		if channel in self.channels:
			self.channels[channel].add_player(player)
		else:
			player.send_message("Channel %s not found." % channel)
	def remove_player_from_channel(self, player, channel="System"):
		if channel in self.channels:
			if channel.remove_player(player):
				del self.channels[channel]
				dm_global.broadcast("Channel %s is vacant, and now will be closed." % channel)
		else:
			player.send_message("Channel %s not found." % channel)
	def get_channels(self):
		s = "List of all channels:"
		for channel in self.channels:
			s += "" + channel.name
		return s
	def remove_player_from_all_channels(self, player):
		for id, channel in self.channels.iteritems():
			channel.remove_player(player)