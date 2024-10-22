import aiohttp
import buttons
from sets import botdata

class Menu:

	async def async_init(self):
		Markup = {'inline_keyboard': [
			[ { 'text': 'Каталог', 'callback_data': 'Каталог' } ]
		]}

		await buttons.send_markup(botdata.MY_ID, Markup, 'Меню:')