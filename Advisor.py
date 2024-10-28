from sets.serverdata import aconexe
from sets import botdata
import asyncio, aiohttp
from UsersDB import UsersDB
from OpenAdviceCom import OpenAdvice
from menu.menu import Menu

# Если запрос от форума --------------------------------------
# Запустить Advisor обработчик -------------------------------
# 
# Если запрос от пользователя (из приватного чата) -----------
# 	Найти пользователя и понять режим пользователя -----------
# 	
# 	Если пользователь в режиме Advisor -----------------------
#		Запустить Advisor обработчик -------------------------
# 	Иначе
# 		Запустить стандартный обработчик ---------------------

class Advisor:

	###############################################################################

	################################### handler ###################################

	###############################################################################

	async def init(self, Query):
		if 'message' in Query:
			if 'is_topic_message' in Query['message']:
				await self.answer_from_topic(Query)
			else:
				await self.question_to_topic(Query)
			return
		if 'callback_query' in Query:
			if 'private' in Query['callback_query']['message']['chat']['type']:
				UserID = Query['callback_query']['message']['chat']['id']
				if Query['callback_query']['data'] == 'order':
					UserData = UsersDB()
					await UserData.init(UserID)
					if UserData.is_advisee(): return
					await OpenAdvice().init(UserID)
					return
				if Query['callback_query']['data'] == 'closeadvise':
					await self.set_default_state(UserID)
					await self.close_topic(UserID)
					await Menu().init(UserID)
					return

	###############################################################################

	################################ class methods ################################

	###############################################################################

	async def set_default_state(self, UserID):
		sql = 'UPDATE `BotUsers` SET appstate = Default WHERE user_id=' + str(UserID) + ';'
		await aconexe(sql)

	async def close_topic(self, UserID):
		TopicID = await self.get_topic_id(UserID)
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'closeforumtopic?' +
				'chat_id=' + botdata.FORUM_ID + '&message_thread_id=' + str(TopicID))

	async def get_user_id(self, TopicID) -> 'is have ? UserID : None':
		sql = 'SELECT user_id FROM BotUsers WHERE topic=' + str(TopicID) + ';'
		fetchall = await aconexe(sql)
		if fetchall: return fetchall[0][0]

	async def answer_from_topic(self, Query):
		import json
		UserID = await self.get_user_id(Query['message']['message_thread_id'])
		if UserID: 
			if self.is_advisor(UserID):
				async with aiohttp.ClientSession() as session:
					Markup = { 'inline_keyboard': [
						[ {'text': 'Закончить обращение', 'callback_data': 'closeadvise' } ]
					] }
					await session.get(botdata.BASE_URL + 'copyMessage?chat_id=' + str(UserID) + 
					'&from_chat_id=' + botdata.FORUM_ID +
					'&message_id=' + str(Query['message']['message_id']) + 
					'&reply_markup=' + json.dumps(Markup))

	async def get_topic_id(self, UserID) -> 'is have ? TopicID : None':
		sql = 'SELECT topic FROM BotUsers WHERE user_id=' + str(UserID) + ';'
		fetchall = await aconexe(sql)
		if fetchall: 
			return fetchall[0][0]

	async def question_to_topic(self, Query):
		TopicID = await self.get_topic_id(Query['message']['from']['id'])
		if TopicID: 
			async with aiohttp.ClientSession() as session:
				await session.get(botdata.BASE_URL + 'copyMessage?chat_id=' + botdata.FORUM_ID + 
				'&message_thread_id=' + str(TopicID) +
				'&from_chat_id=' + str(Query['message']['from']['id']) +
				'&message_id=' + str(Query['message']['message_id']))