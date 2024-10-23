from sets.serverdata import aconexe

class UsersDB:
	async def init(self, UserID):
		sql = 'SELECT * FROM `BotUsers` WHERE user_id=' + str(UserID) + ';'
		fetchall = await aconexe(sql)
		if not fetchall:
			await self.new_user(UserID)
		return fetchall

	async def new_user(self, UserID):
		sql = 'INSERT INTO `BotUsers` (user_id) VALUES (' + str(UserID) + ');'
		await aconexe(sql)