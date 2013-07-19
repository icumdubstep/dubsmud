import dm_global

DIRECTIONS = ['north', 'south', 'east', 'west', 'northeast', 'northwest', 'southeast', 'southwest']
DIRECTION_ALIASES = {

}

def on_connect(player):
	player.room = 'Spawn'
	ROOMS['Spawn'].welcome(player)
def on_disconnect(player):
	ROOMS[player.room].despawn(player)

def addroom(player, args):
	if args not in ROOMS:
		ROOMS[args] = Room(args)
	else:
		player.send_message("A room with that name already exists")
def addexit(player, args):
	if args == "":
		player.send_message("Please enter a direction and a destination.")
		return
	if ' ' not in args:
		player.send_message("Please enter a destination")
		return
	dir = args[:args.index(' ')]
	dest = args[args.index(' ') + 1:]
	if dir not in DIRECTIONS:
		player.send_message("{0} is not a valid direction.".format(dir))
	elif dest not in ROOMS:
		player.send_message("Room '{0}' does not exist.".format(dest))
	else:
		ROOMS[player.room].exits[dir] = Exit(dest)
def changedesc(player, args):
	ROOMS[player.room].description = args
def changelook(player, args):
	ROOMS[player.room].look = args
def look(player, args):
	player.send_message("{0}\n\n{1}\n\nAvailable exits:\n".format(ROOMS[player.room].name, ROOMS[player.room].look))
	for exit, dest in ROOMS[player.room].exits.iteritems():
		player.send_message(exit)

def teleport(player, args):
	if args == "":
		player.send_message("Please enter a destination.")
	elif args in ROOMS:
		ROOMS[player.room].players.remove(player)
		ROOMS[args].welcome(player)
	else:
		player.send_message("Room '{0}' does not exist.".format(args))
def go(player, args):
	if args in ROOMS[player.room].exits:
		ROOMS[player.room].send_to(player, args)
	elif args in DIRECTION_ALIASES and DIRECTION_ALIASES[args] in ROOMS[player.room].exits:
		ROOMS[player.room].send_to(player, DIRECTION_ALIASES[args])
	else:
		player.send_message("Can't go that way")
def say(player, args):
	ROOMS[player.room].send_message("{0} says \"{1}\"".format(player.name, args))
class Room:
	def __init__(self, name):
		self.id = dm_global.NEXT_ROOM_ID
		dm_global.NEXT_ROOM_ID += 1
		self.name = name
		self.look = ""
		self.description = ""
		self.exits = {}
		self.players = []
	def welcome(self, player):
		player.room = self.name
		self.players.append(player)
		player.send_message("{0}\n\n{1}\n\nAvailable exits:\n".format(self.name, self.description))
		for direction, exit in self.exits.iteritems():
			player.send_message(direction)
		self.send_message("{0} trots in.".format(player.name))
	def send_to(self, player, direction):
		self.exits[direction].send_through(player)
		self.players.remove(player)
	def send_message(self, message, exceptions=[]):
		for player in self.players:
			if player.name not in exceptions:
				player.send_message(message)
	def despawn(self, player):
		self.players.remove(player)
		self.send_message("{0} vanishes in a puff of smoke.".format(player.name))
class Exit:
	def __init__(self, destination):
		self.id = dm_global.NEXT_EXIT_ID
		dm_global.NEXT_EXIT_ID += 1
		self.destination = destination
	def send_through(self, player):
		ROOMS[self.destination].welcome(player)
SPAWN = Room("Spawn")
ROOMS = {'Spawn': SPAWN }
COMMANDS = {
	'addroom': (addroom, "Adds a new room", ["ALL"]),
	'addexit': (addexit, "Adds an exit to the current room.", ["ALL"]),
	'changedesc': (changedesc, "Changes the description of the room. This one should be short and to the point.", ["ALL"]),
	'changelook': (changelook, "Changes the 'look' of the room. This one should be detailed.", ["ALL"]),
	'look': (look, "Gives a detailed description of the current room", ["ALL"]),
	'teleport': (teleport, "Teleports to a specified room.", ["ALL"]),
	'go': (go, "Goes in a particular direction", ["ALL"]),
	'say': (say, "Use this to say something in game", ["ALL"])
}