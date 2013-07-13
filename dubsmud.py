#
# dubsmud.py - Main program server loop
#

#imports

from miniboa import TelnetServer
from dm_global import *
import dm_commands, dm_utils


# Length of time in seconds until an idle client is disconnected
IDLE_TIMEOUT = 300

class Player: # class for all connecting users.
	def __init__(self, client, last_channel = "default"):
		self.last_channel = last_channel
		self.client = client
		self.name = "" # blank
		self.status = 0 # login state
		self.admin = False #admin checker
		self.whois = "" #blank
		self.ircmode = False

def process_clients():
	"""
	Check each client, if client.cmd_ready == True then there is a line of
	input available via client.get_command().
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
			player.client.send("Invalid name. No spaces allowed. Try again.")
			player.status = 0
			return
		else:
			player.name = msg
		if player.name == "Admin":
			player.client.send("Hello Admin.  What is your password?\n")
			player.status = 1
			player.client.password_mode_on()
		else:
			CHAT_MANAGER.add_player_to_channel(player)
			
			player.client.send("\nType in 'commands' for a list of available commands.\n> ")
			player.status = 2
			
	elif player.status == 1:
		if msg == "Princess Celestia":
			CHAT_MANAGER.add_player_to_channel(player)
			CHAT_MANAGER.add_player_to_channel(player, "default")
			player.admin = True
			player.client.send("\nType in 'commands' for a list of available commands.\n> ")
			player.status = 2
			
		else:
			player.client.send("Access Denied. Try again.")
			player.status = 0
		player.client.password_mode_off()
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
			CHAT_MANAGER.remove_player_from_all_channels(player)
def on_connect(client):
	"""
	Handles new connections.
	"""
	print "++ Opened connection to %s" % client.addrport()
	player = Player(client)
	PLAYER_LIST.append( Player(client) )
	client.send("Welcome to the DubsMud BBS! \n\n")
	client.send("What is your name? ")

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
    
	print(">> Listening for connections on port %d.  CTRL-C to break."
		% telnet_server.port)

	## Server Loop
	while True:
		try:
			telnet_server.poll()        ## Send, Recv, and look for new connections
			kick_idle()                 ## Check for idle clients
			process_clients()           ## Check for client input
		except dm_utils.ExitSignal as e:
			print e
			cleanup()
			break
	print(">> Server shutdown.")

