from sets.serverdata import aconexe
import asyncio, aiohttp
from sets import botdata

class MessageCounter:
	async def get(self, UserID):
		sql = 'SELECT message_counter FROM BotUsers WHERE user_id = ' + str(UserID) + ';'
		fetchall = await aconexe(sql)
		return fetchall[0][0]

	async def res(self, UserID):
		sql = 'UPDATE BotUsers SET message_counter = DEFAULT WHERE user_id = ' + str(UserID) + ';'
		await aconexe(sql)

	async def set_first(self, UserID, current_MessID: 'current'):
		sql = 'UPDATE BotUsers SET message_counter = ' + str(current_MessID) + ' WHERE user_id = ' + str(UserID) + ';'
		await aconexe(sql)

	async def del_latest(self, UserID, current_MessID):
		first = await self.get(UserID)
		async with asyncio.TaskGroup() as tgdl:
			for x in range(first, current_MessID + 1):
				tgdl.create_task( self.delete_message(UserID, x) )
		await self.res(UserID)

	async def delete_message(self, UserID, MessageID):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'deletemessage?chat_id=' + str(UserID) + '&message_id=' + str(MessageID))