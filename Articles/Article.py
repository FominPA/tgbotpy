from sets import botdata
import asyncio, aiohttp

class Article:
	async def send(self, Query, photo, text):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'sendphoto?chat_id=' + str(Query['message']['chat']['id']) + '&photo=' + str(photo) + str(text))

	async def back_to_general(self, Query, text):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?' + str(text) +
			'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
			'&message_id=' + str(Query['callback_query']['message']['message_id']))