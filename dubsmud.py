from miniboa import TelnetServer

IDLE_TIMEOUT = 300
PLAYER_LIST = []
SERVER_RUN = True

class Player:
    def __init__(self, client):
	self.client = client
	self.handle = "" # blank
	self.status = 0 # login state
	self.admin = False #admin checker
	
class Admin(Player):
    def Player.__init__(self, client):
        self.client = client
        self.handle = "" # blank
        self.status = 0
        self.passwd = "Princess Celestia" #default password, Prompt for change on login
		self.password = ""
def broadcast(msg):
    """
    Send msg to every client.
    """
    for player in PLAYER_LIST:
        player.client.send(msg)

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
    if player.status == 0:
	player.name = msg
		player.client.send("\nType in 'commands' for a list of available commands.\n")
        player.status = 1

	elif player.status == 1 and player.name == "Admin":
	player.client.send("Hello Admin.  What is your password?")
	player.password = msg
		player.client.send("\nType in 'commands' for a list of available commands.\n")
		player.status = 2
		
    else:
        cmd = msg.lower()
        ## bye = disconnect
        if cmd == 'bye':
            player.client.active = False
        ## shutdown == stop the server
        elif cmd == 'shutdown':
            if player.admin == True:
                SERVER_RUN = False #admin tester
            else:
                player.client.send("Permission not granted")
	elif cmd[:4] == 'chat':
	    broadcast("%s : %s\n" % (player.name, msg[4:]))
	elif cmd == 'admin':
		if player.password == player.passwd:
			player.admin = True
		else
			player.client.send("Sorry, permission not granted.")
	elif cmd == 'commands':
	    player.client.send("Available Commands:\nbye\nshutdown\nadmin\nchat\ncommands\n")
def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    print "-- Lost connection to %s" % client.addrport()
    for player in PLAYER_LIST:
	if player.client == client:
        	PLAYER_LIST.remove(player)
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
            print('-- Kicking idle lobby client from %s' % client.addrport())
            player.client.active = False
if __name__ == '__main__':

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
    while SERVER_RUN:
        telnet_server.poll()        ## Send, Recv, and look for new connections
        kick_idle()                 ## Check for idle clients
        process_clients()           ## Check for client input

    print(">> Server shutdown.")

