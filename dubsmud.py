#
# dubsmud.py - Main program server loop
#

# Pre-Alpha

#imports

from miniboa import TelnetServer
from dm_global import *
import dm_commands, dm_utils, dm_chat
import cPickle as pickle


# Length of time in seconds until an idle client is disconnected
IDLE_TIMEOUT = 300

class Player: # class for all connecting users.
	def __init__(self, client, last_channel = "default"):
		self.last_channel = last_channel
		self.client = client
		self.name = "" # blank
		self.description = "" #blank
		self.race = "" #blank
		self.status = 0 # login state
		self.permissions = ["ALL"] # Permission flags
		self.whois = "" #blank
		self.ircmode = False
		self.messages = []
		self.ansi_ui_enabled = False # Flag for the experimental ANSI UI
		self.ansi_color_enabled = True # ANSI colors. Works with pretty much every client, but can be disabled by the user.
		
	# With one exception, this is all you are going to use to send messages to the player.
	def send_message(self, msg):
		if not self.ansi_ui_enabled:
			self.client.send(msg + "\n")
			return

		# Experimental ANSI stuff. Use at your own risk of confusion.
		
		# If we have newline characters, we use our own method of dealing with them.
		if '\n' in msg:
			messages = msg.split('\n')
			for message in messages:
				self.send_message(message) # Recursive call that takes care of newline characters
				
			return
		self.client.send("\x1b[s") # Save the cursor position
		self.messages.append(msg) # Add the message
		# Keep things tidy by adding extra lines for word wrap
		extra_lines = int(len(msg) / 60)
		self.messages.extend([""] * extra_lines)
		x = len(self.messages) - 1
		while x >=100:
			self.messages.pop(0) # We want to keep a cap on the number of messages we keep track of.
			x = x - 1
		while x > 0:
			self.client.send("\x1b[1F") # Go to previous line
			self.client.send("\x1b[2K") # clear it
			self.client.send("\x1b[0G") # move the cursor to column 0
			self.client.send(self.messages[x]) # send the message
			x = x - 1
		self.client.send("\x1b[u") # Restore the cursor position
	def init_screen(self):
		if self.ansi_ui_enabled:
			self.client.send("\x1b[2J\n") # Clear the screen and add newline
			self.send_message("Login Successful")	
def process_clients():
	"""
	Check each client, if client.cmd_ready == True then there is a line of
	input available via client.get_command()
	"""
	for player in PLAYER_LIST:
		if player.client.active and player.client.cmd_ready:
			## If the client sends input, process it.
			process(player)
def process(player):
	"""
	take commands
	"""
	global SERVER_RUN
	msg = player.client.get_command()
	# These statuses are good to use for initial profile creation and login.
	if player.status == 0:
		if ' ' in msg:
			player.send_message("Invalid name. No spaces allowed. Try again.")
			player.status = 0
			return
		else:
			player.name = msg
			
		if player.name == "Admin":
			player.send_message("Hello Admin.  What is your password?\n")
			player.status = 1
			player.client.password_mode_on()
		else:
			player.send_message("Nice name!  I'm...uh, sorry to ask, but are you an earth pony?  Or a pegasus? Or are you a unicorn?")
			player.status = 3

	elif player.status == 1:
		if msg == "Princess Celestia":
			
			CHAT_CHANNELS["System"].add_player(player)
			CHAT_CHANNELS["default"].add_player(player)
			player.permissions.append("ADMINISTRATOR")
			player.send_message("Welcome to the game!\nType in 'commands' for a list of available commands.")
			player.status = 2
			player.init_screen()
			
		else:
			player.send_message("Access Denied. Try again.")
			player.status = 0
		player.client.password_mode_off()
	elif player.status == 3:
                if msg not in ("earth pony", "pegasus", "unicorn"):
                        player.send_message("I'm sorry, please try again.")
                        return
                else:
                        player.race = msg
                        player.send_message("Great!  Now, would you mind describing yourself?\n  What do you look like?  How would a friend describe your nature?")
                        player.status = 4
                                
        elif player.status == 4:
                player.description = msg
                player.status = 5
                
        elif player.status == 5:
                player.send_message("Awesome!  Thanks for putting up with my Luna-damned curiosity, by the way!")
                CHAT_CHANNELS["System"].add_player(player)
		CHAT_CHANNELS["default"].add_player(player)
		player.send_message("Welcome to the game!\nType in 'commands' for a list of available commands.")
		player.status = 2
		player.init_screen()
	else:
		dm_commands.parse_command(player, msg)
	
def on_disconnect(client):
	"""
	Sample on_disconnect function.
	Handles lost connections.
	"""
	print "-- Lost connection to %s" % client.addrport()
	for player in PLAYER_LIST:
		if player.client == client:
        		PLAYER_LIST.remove(player)
			broadcast("{0} has left the server.".format(player.name))
			for cn, channel in CHAT_CHANNELS.iteritems():
				channel.remove_player(player)
def on_connect(client):
	"""
	Handles new connections.
	"""
	print "++ Opened connection to %s" % client.addrport()
	player = Player(client)
	PLAYER_LIST.append( Player(client) )
	client.send("Welcome to the DubsMud BBS! \n\n")
	client.send("What is your name? ")

def collect_players():
        """
        Goes through the PLAYER_LIST and adds each Player to an array of Players
        """
        PLAYER_BOX = ""
        for player in PLAYER_LIST:
                if player.client.active:
                        PLAYER_BOX.append(player)
        pickle.dump( PLAYER_BOX, open( "players.p", "wb" ) )

def kick_idle():
	"""
	Looks for idle clients and disconnects them by setting active to False.
	"""
	## Who hasn't been typing?
	for player in PLAYER_LIST:
		if player.client.idle() > IDLE_TIMEOUT:
			print('-- Kicking idle lobby client from %s' % player.client.addrport())
			player.client.active = False
def cleanup():
	f = open('rules.txt', 'w')
	f.write(RULES)
if __name__ == '__main__':
	f = open('rules.txt', 'r')
	RULES = f.read()
	# Main thread of dubsmud
	telnet_server = TelnetServer(
		port=6380,
		address='',
		on_connect=on_connect,
		on_disconnect=on_disconnect,
		timeout = .05
		)
    	print(" ____      _                   _ \n|    \ _ _| |_ ___ _____ _ _ _| |\n|  |  | | | . |_ -|     | | | . |\n|____/|___|___|___|_|_|_|___|___|\n")
	print(">> Listening for connections on port %d.  CTRL-C to break."
		% telnet_server.port)

	## Server Loop
	while True:
		try:
			telnet_server.poll()        ## Send, Recv, and look for new connections
			kick_idle()                 ## Check for idle clients
			#collect_players()           ## Add to a list of players to stream to a file
			process_clients()           ## Check for client input
		except dm_utils.ExitSignal as e:
			print e
			cleanup()
			break
	print(">> Server shutdown.")

