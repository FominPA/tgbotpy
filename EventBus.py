from requests import get
from sets import botdata
import buttons
from Catalog import Catalog

class EventBus:
	def __init__ (self, Query):
		if 'message' in Query:
			if Query['message']['text'] == '/start':
				self.send_general_menu(Query['message']['from']['id'])
				return

			if Query['message']['text'] == 'Каталог':
				Catalog(Query)
				return

			if Query['message']['text'] == 'Контакт продавца':
				get(botdata.BASE_URL + 'sendcontact?chat_id=' + str(Query['message']['from']['id']) + '&first_name=Никита&last_name=Гифрин&phone_number=79257393984')
				return

			if Query['message']['text'] == 'Закрыть клавиатуру':
				self.remove_keyboard(Query['message']['from']['id'])
				return
		elif 'callback_query' in Query:
			Catalog(Query)


	def send_general_menu(self, UserID):
		Markup = {
			'keyboard': [
				[{'text': 'Каталог'},],
				[{'text': 'Контакт продавца'},],
				[{'text': 'Закрыть клавиатуру'},],
			],
			'resize_keyboard': True
		}

		buttons.send_markup(UserID, Markup)

	def remove_keyboard(self, UserID): buttons.remove_keyboard(UserID)