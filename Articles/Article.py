from sets import botdata
import asyncio, aiohttp

class Article:
	async def send(self, Query, photo, text):
		UserID = 0
		if 'message' in Query:
			UserID = Query['message']['chat']['id']
		elif 'callback_query' in Query:
			UserID = Query['callback_query']['message']['chat']['id']
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'sendphoto?chat_id=' + str(UserID) + '&photo=' + str(photo) + str(text))

	async def back_to_general(self, Query, text):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?' + str(text) +
			'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
			'&message_id=' + str(Query['callback_query']['message']['message_id']))