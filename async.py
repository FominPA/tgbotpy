

# async def get_updates(): return get(botdata.BASE_URL + 'getupdates').json()

# async def main():
# 	# asyncio.TaskGroup().create_task(get_updates())
# 	start = time()
# 	task1 = asyncio.create_task(get_updates())
# 	awaitprint(task1)
# 	print(str(time() - start))

# async def sub():
# 	start = time()
# 	task1 = asyncio.create_task(get_updates())
# 	print(task1)
# 	print(str(time() - start))


# # asyncio.run( main() )
# # print('start sec')
# # asyncio.run( sub() )
# # print('finish')

from requests import get
from time import time, sleep
from os import system
from sets import botdata
from sets.serverdata import con
# from EventBus import EventBus
from EventBus import EventBus
import json
import asyncbuttons as buttons

import aiohttp
import asyncio

def load_last_update_id():
	try:
		with con.cursor() as cursor:
			cursor.execute('SELECT `id` FROM `update_id_log` ORDER BY `date` DESC LIMIT 1;')
			return cursor.fetchall()[0][0]

	except Exception as ex:
		print('func load_last_update_id return error:', str(ex))

# def save_last_update_id(update_id):
# 	try:
# 		with con.cursor() as cursor:
# 			cursor.execute('INSERT INTO `update_id_log` (id, date) VALUES (' + str(update_id) + ', default);')
# 			# cursor.fetchall()

# 	except Exception as ex:
# 		print('func save_last_update_id return error:', str(ex))

def get_updates(): return get(botdata.BASE_URL + 'getupdates').json()

# async def run_eventbus(Query):
# 	await EventBus(Query)

async def streaming_events(array):
	i = 0
	for each in array:
		await asyncio.sleep(0.3)
		# sleep(0.3)
		print('task', i)
		i+=1
	# print (array)

async def start_asyncs_events(matrix):
	async with asyncio.TaskGroup() as tg:
		for each in matrix:
			tg.create_task(streaming_events(matrix[each]))

def parse_to_pool(queries = get_updates()):
	# print(queries['result'])
	matrix = {}
	for query in queries['result']:
		user_id= ''
		if 'message' in query:
			user_id = query['message']['from']['id']
			# print(user_id)
			if user_id in matrix:
				matrix[user_id].append(query)
			else:
				matrix[user_id] = []
				matrix[user_id].append(query)

		if 'callback_query' in query:
			user_id = query['callback_query']['from']['id']
			if user_id in matrix:
				matrix[user_id].append(query)
			else:
				matrix[user_id] = []
				matrix[user_id].append(query)
		# print(matrix[1852081635])

	asyncio.run(start_asyncs_events(matrix))

def listen():
	last_id = load_last_update_id()
	while True:
		for i in range(20):
			query = get_updates()['result']
			tstart = time()
			if query[-1]['update_id'] > last_id:
				pass
				
				# i = 1
				# while query[-i]['update_id'] > last_id:
			# 		# EventBus(query[-i])
			# 		# run usersdb
					# i -= 1
			# 	last_id = query[-1]['update_id']
			# 	save_last_update_id(last_id)
			print(query[-1]['update_id'])
			tfinish = time() - tstart
			if tfinish < 0.5:
				sleep(0.5 - tfinish)
		system('cls')

async def main():

	async with aiohttp.ClientSession() as session:
		async with session.get(botdata.BASE_URL + 'getupdates') as response:

			html = await response.text()
			queries = json.loads(html)['result']
			if 'message' in queries[-1]:
				if queries[-1]['message']['text'] == 'Закрыть клавиатуру':
					await buttons.remove_keyboard(botdata.MY_ID)
					# pass
			# pass

	# async with asyncio.TaskGroup() as tg:
	# 	for i in range(1661, 1645, -1):
	# 		task = tg.create_task(buttons.delete_message(botdata.MY_ID, i))

	# await buttons.remove_keyboard(botdata.MY_ID)
# listen()
# asyncio.run(main())

parse_to_pool()