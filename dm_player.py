#
# dm_player.py - contains the player class
#

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