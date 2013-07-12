from dm_global import *

def parse_msg_irc_mode(player, msg):
	pass
def parse_command(player, msg):
	
	# Distinguish between command and arguments.

	if ' ' in msg:
        	cmd = msg.lower()[:msg.index(' ')]
		args = msg[msg.index(' ') + 1:]
	else:
		# If no arguments, then the command is just the input string.
		cmd = msg.lower()
		args = ""

        # Client commands:

        if cmd == 'quit':
        	player.client.active = False
	elif cmd == 'nick':
		if args == "":
			player.client.send("Enter a new name\n")
	    	else:
			broadcast("%s shall now be known as %s" % (player.name, args))
			player.name = args

        # Admin commands:

        elif cmd == 'shutdown':
        	if player.admin:
                	SERVER_RUN = False #admin tester
        	else:
                	player.client.send("Permission not granted\n")
	elif cmd == 'addch':
		if player.admin:
			if args == "":
				player.client.send("Enter a name for your channel\n")
			else:
				CHAT_MANAGER.add_channel(args)
				broadcast("New channel \"%s\" created.\n" % args)
		else:
			player.client.send("Permission not granted\n")
	elif cmd == 'broadcast':
		if player.admin:
			if args == "":
				player.client.send("Enter a message to broadcast\n")
			else:
				broadcast(args)
		else:
			player.client.send("Permission not granted\n")
	# Chat commands

	elif cmd == 'chat':
		player.client.send(CHAT_MANAGER.handle_message(msg[5:], player))
	
	elif cmd == 'join':
	    	if args == "":
			player.client.send("Enter a channel name\n")
	    	else:
			CHAT_MANAGER.add_player_to_channel(player, args)
	elif cmd == 'part':
	    	if args == "":
			player.client.send("Enter a channel name\n")
	    	else:
			CHAT_MANAGER.remove_player_from_channel(player, args)

	# Help commands

	elif cmd == 'commands':
		player.client.send("Available Commands:\n\nquit\n*shutdown\n*broadcast\nchat\ncommands\n*addch\njoin\npart\nrules\nnick\n\nCommands are not case-sensitive\nStarred commands are admin-only\n")
	elif cmd == 'rules':
		CHAT_MANAGER.display_rules(player)
	# If all else fails....
	else:
		player.client.send("Not a valid command\n")
	player.client.send("> ")