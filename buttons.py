from time import sleep
from requests import get
from sets import botdata
import json

def send_markup(UserID, Markup): return get(botdata.BASE_URL + 'sendMessage?chat_id=' + str(UserID) + '&text=keyboard updated&reply_markup=' + json.dumps(Markup)).json()

def delete_message(UserID, MessageID): get(botdata.BASE_URL + 'deletemessage?chat_id=' + str(UserID) + '&message_id=' + str(MessageID))

def remove_keyboard(UserID):
	Markup = {
		'remove_keyboard': True
	}

	result = send_markup(UserID, Markup)['result']
	# delete_message(UserID, result['message_id'])
	delete_message(UserID, result['message_id'] - 1)