import aiohttp
import buttons
from sets import botdata

class Menu:

	async def init(self, UserID):
		Markup = {'inline_keyboard': [
			[ { 'text': 'Каталог', 'callback_data': 'Каталог' } ],
			[ { 'text': 'Сделать заказ', 'callback_data': 'order' } ],
		]}

		await buttons.send_markup(UserID, Markup, 'Меню:')