global config

config = {
	
	# details required to login to twitch IRC server
	'server': 'irc.chat.twitch.tv',
	'port': 6667,
	'username': 'ShrikeChanBot',
	'oauth_password': 'SECRET', # get this from http://twitchapps.com/tmi/
	
	# channel to join
	#'channels': ['#shrikeg','#bthemeans'],
	'channels': ['#shrikeg'],
	'cron': {
		'#shrikeg': {
			'run_cron': False, 	# set this to false if you want don't want to run the cronjob but you want to preserve the messages etc
			'run_time': 5, 		# time in seconds
			'cron_messages': [
				'This is channel_one cron message one.',
				'This is channel_one cron message two.'
			]
		}
	},

	# if set to true will display any data received
	'debug': False,

	# if set to true will log all messages from all channels
	# todo
	'log_messages': False,

	# maximum amount of bytes to receive from socket - 1024-4096 recommended
	'socket_buffer_size': 2048
}

