"""
Simple IRC Bot for Twitch.tv

Developed by Aidan Thomson <aidraj0@gmail.com>
"""

import lib.irc as irc_
from lib.functions_general import *
import lib.functions_commands as commands

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
from chatterbot.trainers import ListTrainer
FREE_LEARNING = False
chatbot = ChatBot("ShrikeChanBotv3-0", read_only=not FREE_LEARNING,
	storage_adapter='chatterbot.storage.SQLStorageAdapter',
	
    #ogic_adapters=['lib.botchan_adapter.BotChanLogicAdapter'],
	logic_adapters=[
		{
			#'import_path': 'chatterbot.logic.BestMatch',
			'import_path': 'lib.botchan_adapter.BotChanLogicAdapter',
			'maximum_similarity_threshold': 0.6,
		}
	],
	database_uri='sqlite:///databasev3-0.db'
)

class Roboraj:
	
	
	def __init__(self, config):
		self.config = config
		self.irc = irc_.irc(config)
		self.socket = self.irc.get_irc_socket_object()
		self.last_message = ''

	def run(self):
		irc = self.irc
		sock = self.socket
		config = self.config
		ALWAYS_LEARN = False
		while True:
			data = sock.recv(config['socket_buffer_size']).rstrip()

			if len(data) == 0:
				pp('Connection was lost, reconnecting.')
				sock = self.irc.get_irc_socket_object()

			if config['debug']:
				print(data)

			# check for ping, reply with pong
			irc.check_for_ping(data)
			
			if irc.check_for_message(data):
				message_dict = irc.get_message(data)

				channel = message_dict['channel']
				message = message_dict['message']
				username = message_dict['username']
				botCommand = ('@ShrikeChanBot' in message) or ('!learn' in message)
				if username is 'shrikechanbot':
					print('skip bot messages')
				else:
					
					if ALWAYS_LEARN and not botCommand and self.last_message != '':
						clean_message = message.replace('@ShrikeChanBot','').replace('!learn','').strip()
						chatbot.learn_response(Statement(text=clean_message), Statement(text=self.last_message))
						print('LEARNING',clean_message, '>', self.last_message, '=',chatbot.get_response(clean_message))
						self.last_message = clean_message
					ppi(channel, message, username)
					# check if message is a command with no arguments
					if commands.is_valid_command(message) or commands.is_valid_command(message.split(' ')[0]):
						command = message

						if commands.check_returns_function(command.split(' ')[0]):
							if commands.check_has_correct_args(command, command.split(' ')[0]):
								args = command.split(' ')
								del args[0]

								command = command.split(' ')[0]

								if commands.is_on_cooldown(command, channel):
									pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
										command, username, commands.get_cooldown_remaining(command, channel)), 
										channel
									)
								else:
									pbot('Command is valid and not on cooldown. (%s) (%s)' % (
										command, username), 
										channel
									)
									if botCommand:
										args=message
									result = commands.pass_to_function(command, args, chatbot, self.last_message)
									commands.update_last_used(command, channel)

									if result:
										resp = '%s @%s' % (result, username)
										pbot(resp, channel)
										irc.send_message(channel, resp)

						else:
							if commands.is_on_cooldown(command, channel):
								pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
										command, username, commands.get_cooldown_remaining(command, channel)), 
										channel
								)
							elif commands.check_has_return(command):
								pbot('Command is valid and not on cooldown. (%s) (%s)' % (
									command, username), 
									channel
								)
								commands.update_last_used(command, channel)

								resp = '%s @%s' % (commands.get_return(command), username)
								commands.update_last_used(command, channel)

								pbot(resp, channel)
								irc.send_message(channel, resp)
					if ALWAYS_LEARN or botCommand: 
						self.last_message = message.replace('@ShrikeChanBot','').replace('!learn','').strip()
					
