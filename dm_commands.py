#
# dm_commands.py - the file you want to use to make new commands n' stuff
#

from dm_global import *
import dm_utils
import re
import dm_chat

#TODO: proper help topics read from file.

HELP_TOPICS = {
		"": "TOPICS:\n    commands - To see a description of a command, type 'help <command>'\n    formatting - For help on how to format messages.",
		"formatting": "FORMATTING:\nTo activate a particular formatting, enter its character. The formatting will apply to all text entered after the character until the 'clear formatting' character (%)\n\nCharacters:\n    * - bold\n    _ - underline\n    # - invert colors\n    % - clear formatting"
		}

COMMANDS  = []
# Misc Methods
def display_channel_topic(player, channel):
	if channel in CHAT_CHANNELS:
		player.send_message("Topic for {0}: {1}".format((channel, CHAT_CHANNELS[channel].topic)))
	else:
		player.send_message("Channel {0} not found".format(target_channel))


# Command methods
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
def addpubch(player, args):
	if args == "":
			player.send_message("Enter a name for your channel")
	else:
		if ' ' in channel_name:
			return "Channel name invalid"
		elif channel_name in CHAT_CHANNELS:
			return "Channel already open"
		else:
			CHAT_CHANNELS[channel_name] = dm_chat.ChatChannel( True, channel_name )
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
		display_channel_topic(player, player.last_channel)
	else:
		if '@' in args:
			if ' ' in arg
				CHAT_CHANNEL[args[1:(args.index(' '))]].change_topic(player, args[:(args.index(' '))])
			else:
				display_channel_topic(player, args[1:])
		else:
			change_channel_topic(player, player.last_channel, args)
def me(player, args):
	handle_chat_command(player, msg[2:], True)
def join(player, args):
	if args == "":
		player.send_message("Enter a channel name")
	else:
		for channel in args.split(' '):
			if channel in CHAT_CHANNELS:
				CHAT_CHANNELS[channel].add_player(player)
			else:
				player.send_message("Channel %s not found." % channel)
def part(player, args):
	if args == "":
		player.send_message("Enter a channel name")
	else:
		if args == "System":
			player.send_message("Cannot disconnect from System.")
		else:
			for channel in args.split():
				if channel in CHAT_CHANNELS:
					if channel.remove_player(player):
						del CHAT_CHANNELS[channel]
						dm_global.broadcast("Channel %s is vacant, and now will be closed." % channel)
				else:
					player.send_message("Channel %s not found." % channel)
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
	for ch, channel in CHAT_CHANNELS.iteritems():
		player.send_message("{0} - {1}".format(ch, channel.topic))
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
			if channel in CHAT_CHANNELS:
				CHAT_CHANNELS[channel].chat_color = ""
			else:
				player.send_message("Channel %s not found." % channel)
		elif arg in COLORS:
			if arg in COLORS:
				if channel in CHAT_CHANNELS:
					CHAT_CHANNELS[channel].chat_color += COLORS[arg]
				else:
					player.send_message("Channel %s not found." % channel)
			else:
				player.send_message("Color {0} not found.".format(arg))
def showcolors(player, args):
	for color, code in COLORS.iteritems():
		player.send_message("{0}Text\x1b[0m - {1}".format(code, color))
def invite(player, args):
	target_channels = []
	if args == "":
		player.send_message("What users do you want to invite?")
	else:
		for arg in args.split(' '):
			if arg[0] == '@':
				player.last_channel = arg[1:]
				target_channels.append(arg)
			else:
				found = False
				for target_player in PLAYER_LIST:
					if target_player.name == arg:
						CHAT_MANAGER.invite(target_player, target_channels)
						found = True
				if not found:
					player.send_message("Player {0} not found.".format(arg))
				

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
	for channel in target_channels:
		if channel in CHAT_CHANNELS:
			if CHAT_CHANNELS[channel].readonly and "ADMINISTRATOR" not in player.permissions:
				player.send_message("You are not allowed to send messages to this channel.")
			else: 
				if me:
					CHAT_CHANNELS[channel].broadcast("*%s %s" % (player.name, chat_message))
				else:
					CHAT_CHANNELS[channel].broadcast("%s : %s" % (player.name, chat_message))
				player.last_channel = channel
		else:
			return "Channel {0} not found".format(channel)

#
# Dictionary conatining all user methods + descriptions + permission levels indexed by their commands
#

COMMANDS = { 
		'quit': (quit, "Quits. Disconnects from server.", ["ALL"]),
		'nick': (nick, "Nickname command. Use to change your handle.\n\n    Usage: 'nick <new name>'", ["ALL"]),
		'iam': (iam, "Use to change your whois information, or what people will see when they type in \"whois <yourname>\"\n\n    Usage: 'iam <new description>'", ["ALL"]),
		'ansiui': (ansiui, "Toggles experimental ANSI UI. Use at your own risk, not widely supported on MUD clients. Recommended for xterm users. If you don't know what xterm is, this probably is something you should stay away from.", ["ALL"]),
		'shutdown': (shutdown, "Shuts down the MUD. Admin Only", ["ADMINISTRATOR"]),
		'addpubch': (addpubch, "Adds a public chat channel. Only available to moderators and admins", ["ADMINISTRATOR", "MODERATOR"]),
		'broadcast': (broadcast_cmd, "Broadcasts a message to everyone connected to the server. Admin-Only.", ["ADMINISTRATOR"]),
		'chatcolor': (chatcolor, "Changes the color of a public chat channel. Admin/Mod Only", ["ADMINISTRATOR", "MODERATOR"]),
		'ircmode': (ircmode, "Puts your client in irc mode. All commands are preceded with a '/'. Any command not preceded with a slash will be piped as an argument into the 'chat' command.", ["ALL"]),
		'chat': (chat, "Chat command. Use to talk to other players through the chat channels.\n\n    Usage: 'chat [channels] <message>'\n\nIf no channels are specified, then the last channel that the player used will recieve the message.\nIn order to specify a channel, enter in the name of the channel preceded by '@'", ["ALL"]),
		'topic': (topic, "Changes the topic of a public chat channel. Mod/Admin Only", ["ADMINISTRATOR", "MODERATOR"]),
		'me': (me, "Use to denote actions that you take in chat.\n\n    Usage: 'me [channels] <message>'\nIf no channels are specified, then the last channel that the player used will recieve the message.\nIn order to specify a channel, enter in the name of the channel preceded by '@'", ["ALL"]),
		'join': (join, "Join a channel with this command ", ["ALL"]),
		'part': (part, "Leave a channel with this command", ["ALL"]),
		'whois': (whois, "See another user's description", ["ALL"]),
		'msg': (msg, "Message command. Use to message other players privately. \n\n    Usage: 'msg <name> <message>'", ["ALL"]),
		'listchannels': (listchannels, "List all the channels and their topics.", ["ALL"]),
		'commands': (commands, "Displays a list of all commands", ["ALL"]),
		'rules': (rules, "Displays the rules", ["ALL"]),
		'help': (help, "Provides help on a variety of topics.", ["ALL"]),
		'showcolors': (showcolors, "Tests all the colors of the ANSI rainbow.", ["ALL"])
	   }