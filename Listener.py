from requests import get
from time import time, sleep
from os import system
from sets import botdata
from EventBus import EventBus
from EventParser import EventParser

class Listener:
	def __init__(self, sql_con, last_id = 0):
		if last_id == 0:
			last_id = self.load_last_update_id(sql_con)

		while True:
			for _ in range(20):
				queries = self.get_updates()['result']
				tstart = time()
				if not queries:
					try:
						if queries[-1]['update_id'] > last_id:
							unproc = self.select_unproc_queries(queries, last_id)
							EventParser(unproc)
							last_id = queries[-1]['update_id']
							self.save_last_update_id(sql_con, last_id)
					except:
						pass

				# print(queries[-1]['update_id'])
				print(last_id)
				tfinish = time() - tstart
				if tfinish < 0.5:
					sleep(0.5 - tfinish)
			system('cls')

	def load_last_update_id(self, sql_con):
		try:
			with sql_con.cursor() as cursor:
				cursor.execute('SELECT `id` FROM `update_id_log` ORDER BY `date` DESC LIMIT 1;')
				return cursor.fetchall()[0][0]

		except Exception as ex:
			print('func load_last_update_id return error:', str(ex))

	def save_last_update_id(self, sql_con, update_id):
		try:
			with sql_con.cursor() as cursor:
				cursor.execute('INSERT INTO `update_id_log` (id, date) VALUES (' + str(update_id) + ', default);')
				# cursor.fetchall()

		except Exception as ex:
			print('func save_last_update_id return error:', str(ex))

	def get_updates(self): return get(botdata.BASE_URL + 'getupdates').json()

	def select_unproc_queries(self, queries: list, last_id: int):

		unproc = []
		i = -1

		while queries[i]['update_id'] > last_id and i != -len(queries):
			unproc.append(queries[i])
			i -= 1

		unproc.reverse()
		return unproc
