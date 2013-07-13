#
# dm_utils.py - A python file for any miscellaneous junk
#


# ExitSignal Class: An Exception used for the exit in the server loop
#
# If anyone bitches at me for using an exception to exit the program I have the following to say:
#
# 1. A server loop is an iterative algorithm for which the usual case is to continue. Almost all states indicate that the program should continue to iterate over the game loop.
#    "Exit" is an exceptional case. Thus, it is a proper use of the exception.
# 2. Furthermore, since the exception can only be thrown once in the program's runtime, it is also not an inefficient use of the exception.
# 3. The alternative solution does not allow for the flexibility of this solution.

class ExitSignal(Exception): # Throw this at any time during the server loop in order to exit the program
	def __init__(self, code):
		self.code = code
	def __str__(self):
		return "Exit Code: " + repr(self.code)