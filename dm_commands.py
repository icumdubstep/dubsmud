#
# dm_commands.py - the file you want to use to make new commands n' stuff
#

from dm_global import *
import dm_utils
import re

def parse_command(player, msg):
	player.send_message("%s>%s\n" % (player.name, msg))
	if player.ircmode:
		if msg[0] == '/':
			msg = msg[1:]
		else:
			msg = 'chat ' + msg
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
			player.send_message("Enter a new name")
	    	else:
			broadcast("%s shall now be known as %s" % (player.name, args))
			player.name = args
	elif cmd == 'iam':
		if args == "":
			player.send_message("Enter a new whois")
	    	else:
			player.whois = args
			player.send_message("Saved")
        # Admin commands:

        elif cmd == 'shutdown':
        	if player.admin:
                	raise dm_utils.ExitSignal(0)
        	else:
                	player.send_message("Permission not granted")
	elif cmd == 'addch':
		if player.admin:
			if args == "":
				player.send_message("Enter a name for your channel")
			else:
				CHAT_MANAGER.add_channel(args)
				broadcast("New channel \"%s\" created." % args)
		else:
			player.send_message("Permission not granted")
	elif cmd == 'broadcast':
		if player.admin:
			if args == "":
				player.send_message("Enter a message to broadcast")
			else:
				broadcast(args)
		else:
			player.send_message("Permission not granted")
	# Chat commands
	elif cmd == 'ircmode':
		player.ircmode = not player.ircmode
		if player.ircmode:
			player.send_message("IRC mode is ON")
		else:
			player.send_message("IRC mode is OFF")
	elif cmd == 'chat':
		if args == "" or ('@' in args and ' ' not in args):
			if player.ircmode:
				player.send_message("Enter a message. For example:\n    White Power!\nTo direct a message to a particular channel, type @ and the channel's name before the message. For example\n    @snoopdogg Blaze it erryday\n    @bronies @furries ur gay kill urself")
			else:
				player.send_message("Enter a message. For example:\n    chat White Power!\nTo direct a message to a particular channel, type @ and the channel's name before the message. For example\n    chat @snoopdogg Blaze it erryday\n    chat @bronies @furries ur gay kill urself")
	    	else:
			handle_chat_command(player, msg[4:], False)
			
			
	elif cmd == 'me':
		handle_chat_command(player, msg[2:], True)
	elif cmd == 'join':
	    	if args == "":
			player.send_message("Enter a channel name")
	    	else:
			CHAT_MANAGER.add_player_to_channel(player, args)
	elif cmd == 'part':
	    	if args == "":
			player.send_message("Enter a channel name")
	    	else:
			if args == "System":
				player.send_message("Cannot disconnect from System.")
			else:
				CHAT_MANAGER.remove_player_from_channel(player, args)
	elif cmd == 'whois':
		if args == "":
			player.send_message("Enter a name\n")
	    	else:
			found = False
			for target_player in PLAYER_LIST:
				if target_player.name == args:
					found = True
					player.send_message(target_player.whois)
			if not found:
				player.send_message("User not found")
	elif cmd == 'topic':
		if args == "":
			CHAT_MANAGER.display_topic(player, player.last_channel)
	    	else:
			if '@' in args:
				if ' ' in args:
					CHAT_MANAGER.change_topic(player, args[1:(args.index(' '))], args[:(args.index(' '))])
				else:
					CHAT_MANAGER.display_topic(player, args[1:])
			else:
				CHAT_MANAGER.change_topic(player, player.last_channel, args)
	elif cmd == 'msg':
		if args == "":
			player.send_message("Enter a name and a message. For example:\n    msg pinkie_pie ur so sexi")
	    	else:
			if ' ' in args:
				name = args[:msg.index(' ') + 1]
				msg = args[msg.index(' ') + 1:]
			else:
				player.send_message("Enter a message. For example:\n    msg rarity ur so pretti")
			found = False
			for target_player in PLAYER_LIST:
				if target_player.name == name:
					target_player.send_message("%s sends you a message:\n%s\n" % (player.name, msg))
					player.send_message("Message Delivered")
					found = True
			if not found:
				player.send_message("User %s not found" % name)
	elif cmd == 'listchannels':
		player.send_message(CHAT_MANAGER.get_channels())
	# Help commands

	elif cmd == 'commands':
		player.send_message("Available Commands:\n\nquit\n*shutdown\n*broadcast\nchat\nme\nlistchannels\ncommands\n*addch\njoin\npart\nrules\nwhois\niam\nhelp\nmsg\nnick\n\nCommands are not case-sensitive\nStarred commands are admin-only\nTo recieve more detailed information about a command, type in \"command\" and the command. For example: \"help chat\"")
	elif cmd == 'rules':
		player.send_message(RULES)
	elif cmd == 'help':
		player.send_message(get_help(player, args))
	# If all else fails....
	else:
		player.send_message("Not a valid command")
	player.client.send("%s>" % player.name)



def handle_chat_command(player, msg, me=False):
	target_channels = []
	if '@' in msg:
		target_channels_dirty = re.findall(r'@\w+', msg) # regex to find all the channels input into the command
		
		for s in target_channels_dirty:
			target_channels.append(s[1:]) # clean up the preceding '@'s
		# Remove channels from the message
		chat_message = re.sub(r' @\w+', '', msg)
	else:
		target_channels = [player.last_channel]
		chat_message = msg
	# Clean up whitespace
	chat_message = chat_message.strip()
	CHAT_MANAGER.handle_message(chat_message, player, target_channels, me)

def get_help(player, topic):
	if topic == 'help':
		return "BOO! No recursion allowed!"
	elif topic == 'chat':
		return "Chat command. Use to talk to other players through the chat channels.\nUsage: 'chat [channels] <message>'\nIf no channels are specified, then the last channel that the player used will recieve the message.\nIn order to specify a channel, enter in the name of the channel preceded by '@'"
	elif topic == 'msg':
		return "Message command. Use to message other players privately. \nUsage: 'msg <name> <message>'"
	elif topic == 'quit':
		return "Quit command. Disconnects from the server."
	elif topic == 'nick':
		return "Nickname command. Use to change your handle.\nUsage: 'nick <new name>'"
	elif topic == 'iam':
		return ("Use to change your whois information, or what people will see when they type in \"whois %s\"\nUsage: 'iam <new description>'" % player.name)
	elif topic == 'me':
		return "Use to denote actions that you take in chat.\nUsage: 'me [channels] <message>'\nIf no channels are specified, then the last channel that the player used will recieve the message.\nIn order to specify a channel, enter in the name of the channel preceded by '@'"
	else:
		return "Topic not found."