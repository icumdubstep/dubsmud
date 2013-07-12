#
# dm_global.py - The file that stores any data that is global to the dubsmud application
#

# Imports
import dm_chat

# List of all connecting players
PLAYER_LIST = []
# The managing object for all chat.
CHAT_MANAGER = dm_chat.ChatManager()
# Run condition for server loop
SERVER_RUN = True

# global functions

def broadcast(msg):
    """
    Send msg to every client.
    """
    for player in PLAYER_LIST:
        player.client.send(msg)