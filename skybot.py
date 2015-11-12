import Skype4Py
import urllib2
import pickle
import json
import random

class SkyBot:
	
	giphy_api = 'api_key=dc6zaTOxFJmzC'
	host = 'http://api.giphy.com'
	path = '/v1/gifs/random?'
	
	def __init__(self):
		self.skype = Skype4Py.Skype(Events=self)
		self.skype.Attach()
		
	def AttachmentStatus(self, status):
                if status == Skype4Py.apiAttachAvailable:
                        self.skype.attach()
						
	def MessageStatus(self, message, status):
		if status == Skype4Py.cmsReceived or status == Skype4Py.cmsSent:
			splitMessage = message.Body.split()
			for command, function in self.commands.items():
				if command in splitMessage[0]:
					function(self, message)
					break

	def cmdBot(self, message):
		message.Chat.SendMessage('/me Hello, I am SkyBot.')
		
	def cmdGiphy(self, message):
		parts = message.Body.split(' ', 1)
		host = 'http://api.giphy.com'
		path = '/v1/gifs/random?'
		giphy_api = 'api_key=dc6zaTOxFJmzC'
		
		try:
			tagsearch = parts[1].replace(' ','+')
		except IndexError:
			tagsearch = ''
		
		url = host + path + giphy_api + '&tag=' + tagsearch
			
		json_obj = urllib2.urlopen(url)
		
		data = json.load(json_obj)
		
		message.Chat.SendMessage('/me ' + data['data']['image_original_url'])
		
	def cmdSetSticky(self, message):
		global sticky
		sticky = message.Body.split(' ', 1)
		f = open('store.pckl', 'w')
		pickle.dump(sticky[1], f)
		f.close()
		
	def cmdSticky(self, message):
		f = open('store.pckl')
		msg = pickle.load(f)
		f.close()
		message.Chat.SendMessage('/me ' + msg)
	
	def cmdImgur(self, message):
		parts = message.Body.split(' ', 1)
		host = 'https://api.imgur.com/3'
		gallery = '/gallery/t/'
		rand = '/gallery/random/random/'
		
		try:
			tagsearch = parts[1]
		except IndexError:
			tagsearch = ''
			
		if tagsearch == '':
			request = urllib2.Request(host + rand, headers={"Authorization" : "Client-ID 8ff113fdab87a9a"})
		else:	
			request = urllib2.Request(host + gallery + tagsearch, headers={"Authorization" : "Client-ID 8ff113fdab87a9a"})
		
		json_obj = urllib2.urlopen(request)
		
		data = json.load(json_obj)
		randNum = random.randint(0, 50)
		
		if tagsearch == '':
			message.Chat.SendMessage('/me ' + data['data'][randNum]['link'])
		else:
			message.Chat.SendMessage('/me ' + data['data']['items'][random.randint(0,5)]['link'])
		
	def cmdCommands(self, message):
		result = ''
		cmdPrint = {
			'List of commands': '',
			'!giphy <tag>': 'random giphy with optional tag',
			'!imgur <tag>': 'random imgur img with optional tag',
			'!setsticky <text>': 'set the sticky message '		
		}
		
		for item in cmdPrint:
			result += item + ': ' + cmdPrint[item] + '\n' 
		
		#Had to put the sticky message here, skype was detecting it for some reason
		message.Chat.SendMessage('/me ' + result + '!sticky: display sticky message')
		
	commands = {
		'!bot': cmdBot,
		'!giphy': cmdGiphy,
		'!setsticky': cmdSetSticky,
		'!sticky': cmdSticky,
		'!imgur': cmdImgur,
		'!commands': cmdCommands
		}

if __name__ == '__main__':
    bot = SkyBot()
	   
while True:
	skype = Skype4Py.Skype();
	raw_input("prompt: ")