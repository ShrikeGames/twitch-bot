from config.config import *

commands = {
	'!bttv': {
		'limit': 5,
		'argc_all': False,
		'return': 'Better twitch tv emotes available: AYAYA billyReady Clap OMEGALUL PepeHands'
	},
    '!multistream': {
		'limit': 5,
		'argc_all': False,
		'return': 'Watch everyone at the same time: https://multistre.am/shrike/bthemeans/nevturiel/doubleospanky/layout11/ AYAYA'
	},
    '!guess': {
		'limit': 0,
        'argc': 0,
		'argc_all': False,
		'return': 'command'
	},
	'!witcherguess': {
		'limit': 0,
        'argc': 0,
		'argc_all': False,
		'return': 'command'
	},
    '@ShrikeChanBot': {
		'limit': 0,
		'argc': 0,
        'argc_all': True,
		'return': 'command'
	},
	'!learn': {
		'limit': 0,
		'argc': 0,
        'argc_all': True,
		'return': 'command'
	},
	'!nome': {
		'limit': 60,
		'argc_all': False,
		'return': 'no me :)'
	},
	'!play': {
		'limit': 600,
		'argc_all': False,
		'return': '!play'
	}
}


for channel in config['channels']:
	for command in commands:
		commands[command][channel] = {}
		commands[command][channel]['last_used'] = 0
