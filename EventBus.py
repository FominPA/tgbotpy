import asyncio, aiohttp
from sets import botdata
import buttons
from Catalog import Catalog
from UsersDB import UsersDB
from Advisor import Advisor 

# Если запрос от форума --------------------------------------Y
# Запустить Advisor обработчик -------------------------------Y
# 
# Если запрос от пользователя (из приватного чата) -----------Y
# 	Найти пользователя и понять режим пользователя -----------Y
# 	
#	Запустить стандартный обработчик -------------------------Y
# 	Если пользователь в режиме Advisor -----------------------Y
#		Запустить Advisor обработчик -------------------------Y

class EventBus:

	###############################################################################

	################################### handler ###################################

	###############################################################################

	async def init (self, Query: 'json'):

		if 'message' in Query:
			if Query['message']['chat']['type'] == 'supergroup':
				if 'is_topic_message' in Query['message']:
					await Advisor().init(Query)
				return

		UserID = self.get_user_id(Query)

		if 'message' in Query:
			if Query['message']['chat']['type'] == 'private':
				is_have_user_db = await UsersDB().init(UserID)
				from MessageCounter import MessageCounter
				if is_have_user_db:
					if not is_have_user_db[0][3]: # return message_counter
						print(is_have_user_db[0][3])
						await MessageCounter().set_first(UserID, Query['message']['message_id'])
				else:
					await MessageCounter().set_first(UserID, Query['message']['message_id'])

				if 'message' in Query:
					if 'text' in Query['message']:
						if Query['message']['text'] == '/start':
							from menu.menu import Menu
							await Menu().init(Query['message']['from']['id'])
							return
						if Query['message']['text'] == '/clear':
							await MessageCounter().del_latest(UserID, Query['message']['message_id'])
							return

				if is_have_user_db:
					if is_have_user_db[0][1] == 'advisor': # appstate
						await Advisor().init(Query)
						return

		if 'callback_query' in Query:
			if Query['callback_query']['data'] == 'Каталог':
				await Catalog().init(Query)
				return
			if 'editarticle' in Query['callback_query']['data']:
				await Catalog().init(Query)
				return
			if Query['callback_query']['data'] == 'order':
				await Advisor().init(Query)
				return

	###############################################################################

	################################ class methods ################################

	###############################################################################

	def get_user_id(self, Query):
		if 'message' in Query:
			return Query['message']['from']['id']
		else:
			return Query['callback_query']['message']['chat']['id']

	async def send_contact(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'sendcontact?chat_id=' +
			str(Query['message']['from']['id']) + '&first_name=Никита&last_name=Гифрин&phone_number=79257393984')