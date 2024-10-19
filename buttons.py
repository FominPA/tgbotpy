import asyncio, aiohttp
from sets import botdata
import json

async def send_markup(UserID, Markup):
	async with aiohttp.ClientSession() as session:
		await session.get(botdata.BASE_URL + 'sendMessage?chat_id=' + str(UserID) + '&text=keyboard updated&reply_markup=' + json.dumps(Markup))

async def remove_keyboard(UserID):
	Markup = { 'remove_keyboard': True }

	async with aiohttp.ClientSession() as session:
		async with session.get(botdata.BASE_URL + 'sendMessage?chat_id=' + str(UserID) + '&text=keyboard updated&reply_markup=' + json.dumps(Markup)) as response:
			result = await response.text()
			result = json.loads(result)['result']['message_id']
			await delete_message(UserID, result-1)

async def delete_message(UserID, MessageID):
	async with aiohttp.ClientSession() as session:
		await session.get(botdata.BASE_URL + 'deletemessage?chat_id=' + str(UserID) + '&message_id=' + str(MessageID))