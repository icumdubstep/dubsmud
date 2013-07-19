COMMANDS = {

}
class GameState:
	def __init__(self):
		NEXT_EXIT_ID = 0
		NEXT_ROOM_ID = 0
		ROOMS = {}

class Avatar:
	
class Room:
	def __init__(self, name):
		self.id = NEXT_ROOM_ID
		NEXT_ROOM_ID += 1
		self.name = name
		self.description = ""
		self.exits = {}
		self.players = []

class Exit:
	def __init__(self, destination)
		self.id = NEXT_EXIT_ID
		NEXT_EXIT_ID += 1
		self.destination