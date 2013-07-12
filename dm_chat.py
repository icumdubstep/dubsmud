class ChatChannel: # Class for a specific channel for the chat.
	def __init__(self, name="default"):
		self.name = name
		self.connected_players = []
	def broadcast(self, msg):
		for player in self.connected_players:
			player.client.send("%s > %s\n" % (self.name, msg))
	def add_player(self, player):
		if player in self.connected_players:
			player.client.send("Already connected to that channel")
		else:
			self.broadcast("%s connected to %s" % (player.name, self.name) )
			self.connected_players.append(player)
			player.client.send("Connected to {0}\n".format(self.name))
	def remove_player(self, player):
		if player in self.connected_players:
			self.connected_players.remove(player)
			self.broadcast("%s disconnected from %s" % (player.name, self.name) )
			player.client.send("Disconnected from {0}\n".format(self.name))
		else:
			player.client.send("Not connected to {0}\n".format(self.name))
class ChatManager:
	def __init__(self):
		self.channels = [ChatChannel()]
		f = open('help.txt', 'r')
		self.rules = f.read()
	def add_channel(self, channel_name="default"):
		for channel in self.channels:
			if channel.name == channel_name:
				return "Channel already open\n"
		self.channels.append( ChatChannel( channel_name ) )
	def handle_message(self, msg, player):
		channel_specified = msg[:1] == "@"
		if channel_specified:
			target_channel = msg[1:(msg.index(' '))]
			
		else:
			target_channel = player.last_channel
		channel_found = False
		for channel in self.channels:
			if channel.name == target_channel:
				if channel_specified:
					channel.broadcast("%s : %s" % (player.name, msg[msg.index(' ') + 1:]))
					player.last_channel = target_channel
				else: 
					channel.broadcast("%s : %s" % (player.name, msg))
				channel_found = True
				
		if not channel_found:
			return "Channel {0} not found".format(target_channel)
	def add_player_to_channel(self, player, channel_name="default"):
		for channel in self.channels:
			if channel.name == channel_name:
				channel.add_player(player)
				return
		player.client.send("Channel %s not found.\n" % channel_name)
	def remove_player_from_channel(self, player, channel_name="default"):
		for channel in self.channels:
			if channel.name == channel_name:
				channel.remove_player(player)
				return
		player.client.send("Channel %s not found.\n" % channel_name)
	def remove_player_from_all_channels(self, player):
		for channel in self.channels:
			channel.remove_player(player)
	def display_rules(self, player):
		player.client.send(self.rules)