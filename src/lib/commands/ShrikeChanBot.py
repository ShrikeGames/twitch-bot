# coding: utf8
import traceback
import requests, random
from chatterbot.conversation import Statement
def ShrikeChanBot(args, chatbot, last_message):
	
	message = args[len('@ShrikeChanBot'):].strip()
	print('message',message)
	print('last_message',last_message)
	try:
		response = chatbot.get_response(message)
		if response:
			return str(response.text)
		else:
			return 'I have no idea!'
	except Exception as e:
		traceback.print_exc()
		return 'AYAYA An error occured'

