import asyncio, aiohttp
from sets import botdata
import buttons
from Catalog import Catalog

class EventBus:
	async def init (self, Query):
		if 'message' in Query:
			if Query['message']['text'] == '/start':
				await self.send_general_menu(Query['message']['from']['id'])

			if Query['message']['text'] == 'Каталог':
				await Catalog.init(None, Query)

			if Query['message']['text'] == 'Контакт продавца':
				await self.send_contact(Query)

			if Query['message']['text'] == 'Закрыть клавиатуру':
				await self.remove_keyboard(Query['message']['from']['id'])
		elif 'callback_query' in Query:
			await Catalog.init(None, Query)


	async def send_general_menu(self, UserID):
		Markup = {
			'keyboard': [
				[{'text': 'Каталог'},],
				[{'text': 'Контакт продавца'},],
				[{'text': 'Закрыть клавиатуру'},],
			],
			'resize_keyboard': True
		}

		await buttons.send_markup(UserID, Markup)

	async def remove_keyboard(self, UserID): await buttons.remove_keyboard(UserID)

	async def send_contact(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'sendcontact?chat_id=' + str(Query['message']['from']['id']) + '&first_name=Никита&last_name=Гифрин&phone_number=79257393984')