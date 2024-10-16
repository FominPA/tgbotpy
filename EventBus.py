from requests import get
import botdata
import buttons
from LifePO4 import LifePO4
from YZPower import YZPower
from BMSDaly import BMSDaly

class EventBus:
	def __init__ (self, Query):
		if 'message' in Query:
			if Query['message']['text'] == '/start':
				self.send_general_menu(Query['message']['from']['id'])
				return

			if Query['message']['text'] == 'Каталог':
				LifePO4(Query)
				YZPower(Query)
				BMSDaly(Query)
				return

			if Query['message']['text'] == 'Контакт продавца':
				get(botdata.BASE_URL + 'sendcontact?chat_id=' + str(Query['message']['from']['id']) + '&first_name=Никита&last_name=Гифрин&phone_number=79257393984')
				return

			if Query['message']['text'] == 'Закрыть клавиатуру':
				self.remove_keyboard(Query['message']['from']['id'])
				return
		elif 'callback_query' in Query:
			LifePO4(Query)
			BMSDaly(Query)
			YZPower(Query)


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