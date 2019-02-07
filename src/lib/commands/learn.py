# coding: utf8

import requests, random
from chatterbot import ChatBot
from chatterbot.conversation import Statement

def learn(args, chatbot, last_message):
	
	message = args[len('!learn'):].strip()
	#try:
	if last_message != '':
		
		previous=last_message
		if 'I am sorry, but I do not understand.' not in message:
			chatbot.read_only = False
			chatbot.learn_response(Statement(text=message), Statement(text=previous))
			chatbot.read_only = True
			#return response
			return 'I have learned to respond to '+previous+' with '+ str(message)
		return 'Hm, I cannot learn that'
	else:
		return 'AYAYA Ask me something first'
	#except Exception as e:
	#	return 'AYAYA An error occured'
