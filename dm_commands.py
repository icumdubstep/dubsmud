#
# dm_commands.py - the file you want to use to make new commands n' stuff
#

from dm_global import *
import dm_utils
import re

#TODO: proper help topics read from file.

HELP_TOPICS = {"": "TOPICS:\ncommands - To see a description of a command, type 'help <command>'"}

COMMANDS  = []

def quit(player, args):
	player.client.active = False

def nick(player, args):
	if args == "":
		player.send_message("Enter a new name")
	else:
		broadcast("%s shall now be known as %s" % (player.name, args))
		player.name = args
def iam(player, args):
	if args == "":
		player.send_message("Enter a new whois")
	else:
		player.whois = args
		player.send_message("Saved")
def ansiui(player, args):
	if player.ansi_ui_enabled:
		player.ansi_ui_enabled = False
		player.send_message("ANSI UI disabled")
	else:
		player.ansi_ui_enabled = True
		player.init_screen()
		player.send_message("ANSI UI enabled")
def shutdown(player, args):
        raise dm_utils.ExitSignal(0)
def addch(player, args):
	if args == "":
			player.send_message("Enter a name for your channel")
	else:
		CHAT_MANAGER.add_channel(args)
		broadcast("New channel \"%s\" created." % args)
def broadcast_cmd(player, args):
	if args == "":
		player.send_message("Enter a message to broadcast")
	else:
		broadcast(args)
	
def ircmode(player, args):
	player.ircmode = not player.ircmode
	if player.ircmode:
		player.send_message("IRC mode is ON")
	else:
		player.send_message("IRC mode is OFF")
def chat(player, args):
	if args == "" or ('@' in args and ' ' not in args):
		if player.ircmode:
			player.send_message("Enter a message. For example:\n    White Power!\nTo direct a message to a particular channel, type @ and the channel's name before the message. For example\n    @snoopdogg Blaze it erryday\n    @bronies @furries ur gay kill urself")
		else:
			player.send_message("Enter a message. For example:\n    chat White Power!\nTo direct a message to a particular channel, type @ and the channel's name before the message. For example\n    chat @snoopdogg Blaze it erryday\n    chat @bronies @furries ur gay kill urself")
	else:
		handle_chat_command(player, args, False)
def topic(player, args):
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
def me(player, args):
	handle_chat_command(player, msg[2:], True)
def join(player, args):
	if args == "":
		player.send_message("Enter a channel name")
	else:
		CHAT_MANAGER.add_player_to_channel(player, args)
def part(player, args):
	if args == "":
		player.send_message("Enter a channel name")
	else:
		if args == "System":
			player.send_message("Cannot disconnect from System.")
		else:
			CHAT_MANAGER.remove_player_from_channel(player, args)
def whois(player, args):
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
def msg(player, args):
	if args == "":
		player.send_message("Enter a name and a message. For example:\n    msg pinkie_pie ur so sexi")
	else:
		if ' ' in args:
			name = args[:args.index(' ') + 1]
			msg = args[args.index(' ') + 1:]
		else:
			player.send_message("Enter a message. For example:\n    msg rarity ur so pretti")
			return
		found = False
		for target_player in PLAYER_LIST:
			if target_player.name == name:
				target_player.send_message("%s sends you a message:\n%s\n" % (player.name, msg))
				player.send_message("Message Delivered")
				found = True
		if not found:
			player.send_message("User %s not found" % name)
def listchannels(player, args):
	player.send_message(CHAT_MANAGER.get_channels())
def commands(player, args):
	player.send_message("Available Commands:")
	for cmd_name, cmd in COMMANDS.iteritems():
		if set(COMMANDS[cmd_name][2]).intersection( set(player.permissions) ):
			player.send_message("{0}".format(cmd_name))
	player.send_message("\nCommands are not case-sensitive\nStarred commands are admin-only\nTo recieve more detailed information about a command, type in \"help\" and the command. For example: \"help chat\"")
def rules(player, args):
	player.send_message(RULES)
def help(player, args):
	if args in COMMANDS:
		player.send_message(COMMANDS[args][1])
	elif args in HELP_TOPICS:
		player.send_message(HELP_TOPICS[args])
	else:
		player.send_message("Topic not found")
def chatcolor(player, args):
	current_channel = player.last_channel
	args_list = args.split(' ')
	for arg in args_list:
		if arg[0] == '@':
			current_channel = arg[1:]
			CHAT_MANAGER.clear_color(current_channel, player)
		elif arg in COLORS:
			CHAT_MANAGER.add_color(current_channel, COLORS[arg], player)
#
# parse_command - called by dubsmud.py to process whatever command the user puts in.
#

def parse_command(player, msg):
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

        

        if cmd in COMMANDS:
		if set(COMMANDS[cmd][2]).intersection( set(player.permissions) ):
			COMMANDS[cmd][0](player, args)
		else:
			player.send_message("You don't have permission to do that.")
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


#
# Dictionary conatining all user methods + descriptions + permission levels indexed by their commands
#

COMMANDS = { 
		'quit': (quit, "Quits. Disconnects from server.", ["ALL"]),
		'nick': (nick, "Nickname command. Use to change your handle.\nUsage: 'nick <new name>'", ["ALL"]),
		'iam': (iam, "Use to change your whois information, or what people will see when they type in \"whois <yourname>\"\nUsage: 'iam <new description>'", ["ALL"]),
		'ansiui': (ansiui, "", ["ALL"]),
		'shutdown': (shutdown, "", ["ADMINISTRATOR"]),
		'addch': (addch, "", ["ADMINISTRATOR", "MODERATOR"]),
		'broadcast': (broadcast_cmd, "", ["ADMINISTRATOR"]),
		'chatcolor': (chatcolor, "", ["ADMINISTRATOR", "MODERATOR"]),
		'ircmode': (ircmode, "", ["ALL"]),
		'chat': (chat, "Chat command. Use to talk to other players through the chat channels.\nUsage: 'chat [channels] <message>'\nIf no channels are specified, then the last channel that the player used will recieve the message.\nIn order to specify a channel, enter in the name of the channel preceded by '@'", ["ALL"]),
		'topic': (topic, "", ["ALL"]),
		'me': (me, "Use to denote actions that you take in chat.\nUsage: 'me [channels] <message>'\nIf no channels are specified, then the last channel that the player used will recieve the message.\nIn order to specify a channel, enter in the name of the channel preceded by '@'", ["ALL"]),
		'join': (join, "", ["ALL"]),
		'part': (part, "", ["ALL"]),
		'whois': (whois, "", ["ALL"]),
		'msg': (msg, "Message command. Use to message other players privately. \nUsage: 'msg <name> <message>'", ["ALL"]),
		'listchannels': (listchannels, "", ["ALL"]),
		'commands': (commands, "", ["ALL"]),
		'rules': (rules, "", ["ALL"]),
		'help': (help, "", ["ALL"])
		
	   }