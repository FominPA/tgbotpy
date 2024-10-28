import asyncio, aiohttp
import buttons
from sets import botdata
from sets.serverdata import aconexe
from urllib.parse import quote

class OpenAdvice:
	""" Command :: create or reopen advice & set appstate 'advisor' """

	###############################################################################

	################################### handler ###################################

	###############################################################################

	async def init(self, UserID):
		await self.set_advisor_state(UserID) # DB
		TopicID = await self.get_topic_id(UserID) # DB
		if TopicID:
			await self.reopen_advice(TopicID) # TG
		else:
			TopicID = await self.create_topic(UserID) # TG
			await self.write_new_topic(UserID, TopicID) # DB
		await self.hello_message(UserID) # TG

	async def set_advisor_state(self, UserID):
		sql = 'UPDATE `BotUsers` SET appstate = \'advisor\' WHERE user_id=' + str(UserID) + ';'
		await aconexe(sql)

	###############################################################################

	################################ class methods ################################

	###############################################################################

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

	async def hello_message(self, UserID):
		text = quote('Создано новое обращение:\n\n' +
		'Задайте ваш вопрос, и продавец на него ответят')

		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'sendMessage?chat_id=' + str(UserID) + 
			"&text=" + str(text) + '&parse_mode=html')

	async def reopen_advice(self, TopicID):
		async with aiohttp.ClientSession() as session:
			print (botdata.BASE_URL + 'reopenForumTopic?chat_id=' + 
			botdata.FORUM_ID + '&message_thread_id=' + str(TopicID))
			await session.get(botdata.BASE_URL + 'reopenForumTopic?chat_id=' + 
			botdata.FORUM_ID + '&message_thread_id=' + str(TopicID))
