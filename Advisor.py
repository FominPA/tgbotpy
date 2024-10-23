from sets.serverdata import aconexe
from sets import botdata
import asyncio, aiohttp
import buttons
from UsersDB import UsersDB
from urllib.parse import quote

class OpenAdvice:
	""" Command :: create or reopen advice & set appstate 'advisor' """
	async def init(self, UserID):
		await self.set_advisor_state(UserID) # DB
		TopicID = await self.get_topic_id(UserID) # DB
		if TopicID:
			await self.reopen_advice(UserID) # TG
		else:
			TopicID = await self.create_topic(UserID) # TG
			await self.write_new_topic(UserID, TopicID) # DB
		await self.end_advice_button(UserID) # TG

	async def set_advisor_state(self, UserID):
		sql = 'UPDATE `BotUsers` SET appstate = \'advisor\' WHERE user_id=' + str(UserID) + ';'
		await aconexe(sql)

	# Создать топик с обращением
	async def create_topic(self, UserID) -> 'TopicID: chat_id':
		result = None
		async with aiohttp.ClientSession() as session:
			async with session.get(botdata.BASE_URL + 
			'createForumTopic?chat_id=' + botdata.FORUM_ID +
			'&name=Обращение от пользователя: ' + str(UserID)) as response:
				result = await response.json()
		if result['ok']:
			return result['result']['message_thread_id']

	# Записать топик в БД
	async def write_new_topic(self, UserID, TopicID):
		sql = 'UPDATE `BotUsers` set topic=' + str(TopicID) + ' WHERE user_id=' + str(UserID) + ';'
		await aconexe(sql)

	# Async скрипт нового обращения
	async def new_advice_group(self, UserID):
		TopicID = await self.create_topic(UserID)
		await self.write_new_topic(UserID, TopicID)

	async def get_topic_id(self, UserID) -> 'is have ? TopicID : None':
		sql = 'SELECT topic FROM BotUsers WHERE user_id=' + str(UserID) + ';'
		fetchall = await aconexe(sql)
		if fetchall: 
			return fetchall[0][0]

	async def end_advice_button(self, UserID):
		header = quote('Создано новое обращение:\n\n' +
		'Задайте ваш вопрос, и наши специалисты на него ответят или нажмите \"Закончить диалог\", чтобы вернуться к меню')
		header += '&parse_mode=html'
		Markup = {
			'keyboard': [
				[{'text': 'Закончить диалог'},]
			],
			'resize_keyboard': True,
			'one_time_keyboard': True
		}
		await buttons.send_markup(UserID, Markup, header)

	async def reopen_advice(self, TopicID):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'reopenForumTopic?chat_id=' + 
			botdata.FORUM_ID + '&message_thread_id=' + str(TopicID))

class Advisor:
	async def init(self, Query):
		if 'message' in Query:
			if 'is_topic_message' in Query['message']:
				await self.answer_from_topic(Query)
				return
			elif Query['message']['text'] == 'Закончить диалог':
				await self.set_default_state(UserID = Query['message']['chat']['id'])
				await self.close_topic(UserID = Query['message']['chat']['id'])
				return
			else:
				await self.question_to_topic(Query)
				return
		elif 'callback_query' in Query:
			UserID = Query['callback_query']['message']['chat']['id']
			if Query['callback_query']['data'] == 'order':
				fetchall = await UsersDB().init(UserID)
				if fetchall:
					if fetchall[0][1] == 'advisor':
						return None
				await OpenAdvice().init(UserID)
				return
			elif Query['callback_query']['data'] == 'closeadvise':
				await self.set_default_state(UserID)
				await self.close_topic(UserID)
				return

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
		UserID = await self.get_user_id(Query['message']['message_thread_id'])
		if UserID: 
			async with aiohttp.ClientSession() as session:
				await session.get(botdata.BASE_URL + 'copyMessage?chat_id=' + str(UserID) + 
				'&from_chat_id=' + botdata.FORUM_ID +
				'&message_id=' + str(Query['message']['message_id']))

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