from EventBus import EventBus
import asyncio, aiohttp

# > Принимает список запросов
# > Разбивает список на пользователей
# > Для каждого пользователя запускает собственный поток
#   обработки запросов

class EventParser:
	def __init__ (self, queries: list) -> None:
		UD = self.split_users(queries)
		asyncio.run(self.run_users_streams(UD))

	def split_users(self, queries: list) -> 'Dict of lists':
		users_dict = {}
		for query in queries:
			if 'message' in query:
				user_id = query['message']['from']['id']
				if user_id in users_dict:
					users_dict[user_id].append(query)
				else:
					users_dict[user_id] = []
					users_dict[user_id].append(query)

			if 'callback_query' in query:
				user_id = query['callback_query']['from']['id']
				if user_id in users_dict:
					users_dict[user_id].append(query)
				else:
					users_dict[user_id] = []
					users_dict[user_id].append(query)
		return users_dict
		
	# создаёт параллельную обработку очередей для каждого пользователя
	async def run_users_streams(self, users_dict: 'Dict of users queue'):
		async with asyncio.TaskGroup() as tg:
			for user in users_dict:
				tg.create_task(self.run_queries_stream(users_dict[user]))

	# Принимает очередь запросов от одного пользователя и запускает их
	async def run_queries_stream(self, queries: list):
		for each in queries:
			await EventBus().init(each)