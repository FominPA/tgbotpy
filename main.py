from requests import get
from time import sleep
from os import system
import botdata
from serverdata import con
from EventBus import EventBus

def load_last_update_id():
	try:
		with con.cursor() as cursor:
			cursor.execute('SELECT `id` FROM `update_id_log` ORDER BY `date` DESC LIMIT 1;')
			return cursor.fetchall()[0][0]

	except Exception as ex:
		print('func load_last_update_id return error:', str(ex))

def save_last_update_id(update_id):
	try:
		with con.cursor() as cursor:
			cursor.execute('INSERT INTO `update_id_log` (id, date) VALUES (' + str(update_id) + ', default);')
			# cursor.fetchall()

	except Exception as ex:
		print('func save_last_update_id return error:', str(ex))

def get_updates(): return get(botdata.BASE_URL + 'getupdates').json()

last_id = load_last_update_id()
while True:
	for i in range(20):
		query = get_updates()['result']
		if query[-1]['update_id'] > last_id:
			i = 1
			while query[-i]['update_id'] > last_id:
				# run eventbus
				EventBus(query[-i])
				# run usersdb
				i -= 1
			last_id = query[-1]['update_id']
			save_last_update_id(last_id)
		print(query[-1]['update_id'])
		sleep(0.5)
	system('cls')
