from sets.serverdata import aconexe
import asyncio

class UsersDB:
	concrete_user = None

	###############################################################################

	################################### handler ###################################

	###############################################################################

	async def init(self, UserID):
		concrete_user = await self.get_user_all(UserID)
		if not concrete_user:
			await self.new_user(UserID)
		return concrete_user

	###############################################################################

	################################ class methods ################################

	###############################################################################

	async def new_user(self, UserID):
		sql = 'INSERT INTO `BotUsers` (user_id) VALUES (' + str(UserID) + ');'
		await aconexe(sql)

	async def get_user_all(self, UserID) -> 'list in list':
		sql = 'SELECT * FROM `BotUsers` WHERE user_id=' + str(UserID) + ';'
		concrete_user = await aconexe(sql)
		if concrete_user:
			concrete_user =  self.parse_user_info(concrete_user)

	def parse_user_info(self, fetchall: 'list in list'):
		fetchall = fetchall[0]
		return {
			'user_id': fetchall[0],
			'appstate': fetchall[1],
			'topic': fetchall[2],
			'message_counter': fetchall[3]
		}

	def message_counter_setted(self):
		if concrete_user:
			if concrete_user['message_counter']: 
				return True
		return False

	def is_advisee(self):
		if concrete_user:
			if concrete_user['appstate'] == 'advisor': 
				return True
		return False