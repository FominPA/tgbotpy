import asyncio, aiohttp
from sets import botdata
import buttons
from Catalog import Catalog
from menu.menu import Menu
from UsersDB import UsersDB
from Advisor import Advisor 

class EventBus:
	async def init (self, Query):
		if 'message' in Query:
			if 'is_topic_message' in Query['message']:
				await Advisor().init(Query)
				return
		# else:
		UserID = self.get_user_id(Query)
		fetchall = await UsersDB().init(UserID)
		if fetchall:
			if fetchall[0][1] == 'advisor':
				await Advisor().init(Query)
				return
			elif UserID:
				if 'message' in Query:
					if 'text' in Query['message']:
						if Query['message']['text'] == '/start':
							await Menu.async_init(None, Query['message']['from']['id'])

						if Query['message']['text'] == 'Каталог':
							await Catalog.init(None, Query)

						if Query['message']['text'] == 'Контакт продавца':
							await self.send_contact(Query)
				elif 'callback_query' in Query:
					if Query['callback_query']['data'] == 'Каталог':
						await Catalog.init(None, Query)
						return
					if 'editarticle' in Query['callback_query']['data']:
						await Catalog.init(None, Query)
						return
					if Query['callback_query']['data'] == 'order':
						await Advisor().init(Query)

	def get_user_id(self, Query):
		if 'message' in Query:
			return Query['message']['from']['id']
		else:
			return Query['callback_query']['message']['chat']['id']

	async def send_general_menu(self, UserID):
		Markup = {
			'keyboard': [
				[{'text': 'Каталог'},],
				[{'text': 'Контакт продавца'},],
			],
			'resize_keyboard': True
		}

		await buttons.send_markup(UserID, Markup)

	async def remove_keyboard(self, UserID): await buttons.remove_keyboard(UserID)

	async def send_contact(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'sendcontact?chat_id=' + str(Query['message']['from']['id']) + '&first_name=Никита&last_name=Гифрин&phone_number=79257393984')