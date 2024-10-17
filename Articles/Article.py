from requests import get
from sets import botdata

class Article:

	def send(self, Query, photo, text):
		get(botdata.BASE_URL + 'sendphoto?chat_id=' + str(Query['message']['chat']['id']) + '&photo=' + str(photo) + str(text))

	def back_to_general(self, Query, text):
		get(botdata.BASE_URL + 'editMessagecaption?' + str(text) +
			'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
			'&message_id=' + str(Query['callback_query']['message']['message_id'])
		)