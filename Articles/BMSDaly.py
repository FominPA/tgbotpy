import json
from sets import botdata
from Articles.Article import Article
import asyncio, aiohttp
from urllib.parse import quote

class BMSDaly(Article):
	ucode = '1285651'
	
	async def init (self, Query):
		if 'message' in Query:
			if Query['message']['text'] == 'Каталог':
				await super().send(Query, self.get_photo(), self.get_general_text())
		elif 'callback_query' in Query:
			if 'Каталог' in Query['callback_query']['data']:
				await super().send(Query, self.get_photo(), self.get_general_text())
			if self.ucode in Query['callback_query']['data']:
				if 'general' in Query['callback_query']['data']:
					await super().back_to_general(Query, self.get_general_text())
				if 'more' in Query['callback_query']['data']:
					await self.more(Query)
				if 'stock' in Query['callback_query']['data']:
					await self.stock(Query)
				if 'v12' in Query['callback_query']['data']:
					await self.v12(Query)
				if 'v24' in Query['callback_query']['data']:
					await self.v24(Query)
				if 'v36' in Query['callback_query']['data']:
					await self.v36(Query)
				if 'v48' in Query['callback_query']['data']:
					await self.v48(Query)
				if 'v60' in Query['callback_query']['data']:
					await self.v60(Query)

	def get_photo(self): return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRi8FQHeWvp_yikhJWqCMIF1glkoy2HWvr28A&s'

	def get_general_text(self): 
		return ('&caption=' +
			quote('<b>⚡️⚡️⚡️⚡️ Плaтa BMS Daly ⚡️⚡️⚡️⚡️</b>\n' +
			'\n' +
			'Плaты ВМS для LiFeРO4 аккумуляторoв 12, 24, 36, 48, 60 В (4S, 8S, 12S, 16S, 20S) \n' +
			'нa тoки oт 20 до 250 A\n') +
			'&parse_mode=html' +
			'&reply_markup=' +
			json.dumps({
				'inline_keyboard': 
					[[{'text': 'Подробнее', 'callback_data': self.ucode + 'more'},],]
			}))

	async def send(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'sendphoto?chat_id=' + str(Query['message']['chat']['id']) + 
				'&photo=' + self.get_photo() + self.get_general_text())

	async def back_to_general(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?' +
				self.get_general_text() +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def more(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' + quote(
				'⚡️⚡️⚡️ Плaтa BMS ⚡️⚡️⚡️\n' +
				'\n' +
				'Hовые платы ВМS от фирмы DАLY для LiFePО4 батаpей – вaжнейший компонeнт кaчественнoго аккумуляторa. \n' +
				'\n' +
				'Дaнные платы являются проверенными качественными продуктами, их используют в большинстве современных LiFеРО4 аккумуляторах. \n' +
				'\n' +
				'Платы влагозащищенные, что позволяет использовать их в местах с повышенной влажностью, например, в АКБ для лодок и катеров.\n' +
				'\n' +
				'Все платы симметричные, в комплекте идет шлейф для подключения к элементам АКБ, а для смарт версий еще и датчик Вluеtооth.\n' +
				'\n' +
				'📦 ДОСТАВКА: Транспортными компаниями\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
							[ {'text': 'Наличие и цены', 'callback_data': self.ucode + 'stock'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def stock(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' +
				quote('⚡️⚡️⚡️ Плaтa BMS ⚡️⚡️⚡️\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'Выберите количество В вашей сети\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'<b>Также доступны аксессуары к платам БМС DАLY:</b>\n' +
				'\n' +
				'• Кабель UАRТ – 800 руб.\n' +
				'• Кабель 485 – 900 руб.\n' +
				'• Шина САN – 4 700 руб.\n' +
				'• Датчик заряда (прямоугольный) – 800 руб.\n' +
				'• Датчик заряда (круглый) – 1 000 руб.\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ 
								{'text': '12B', 'callback_data': self.ucode + 'v12'}, 
								{'text': '24B', 'callback_data': self.ucode + 'v24'}, 
								{'text': '36B', 'callback_data': self.ucode + 'v36'}, 
								{'text': '48B', 'callback_data': self.ucode + 'v48'}, 
								{'text': '60B', 'callback_data': self.ucode + 'v60'}, 
							],
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
							[ {'text': 'Подробнее', 'callback_data': self.ucode + 'more'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def v12(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' +
				quote('⚡️⚡️⚡️ Плaтa BMS ⚡️⚡️⚡️\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'✅ В НАЛИЧИИ:\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'<b>Платы на 12В аккумуляторы (4S, 14.6V):</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 4S * 12V * 20А – <b>1000 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 4S * 12V * 40А – <b>1400 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 4S * 12V * 80А – <b>3100 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 4S * 12V * 150А – <b>6500 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 4S * 12V * 200А – <b>9800 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 4S * 12V * 250А – <b>10900 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 4S * 12V * 100А – <b>5600 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 4S * 12V * 200А – <b>10500 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 4S * 12V * 250А – <b>11500 р.</b>\n' +
				'Плата Dаly ВМS (К-тип смарт): LiFеРО4 * 4S * 12V * 60А – <b>4100 р.</b>\n' +
				'Плата Dаly ВМS (К-тип смарт): LiFеРО4 * 4S * 12V * 100А – <b>5600 р.</b>\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ 
								{'text': '↩', 'callback_data': self.ucode + 'stock'},
								{'text': '24B', 'callback_data': self.ucode + 'v24'}, 
								{'text': '36B', 'callback_data': self.ucode + 'v36'}, 
								{'text': '48B', 'callback_data': self.ucode + 'v48'}, 
								{'text': '60B', 'callback_data': self.ucode + 'v60'}, 
							],
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def v24(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' +
				quote('⚡️⚡️⚡️ Плaтa BMS ⚡️⚡️⚡️\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'✅ В НАЛИЧИИ:\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'<b>Платы на 24В аккумуляторы (8S, 29.2V):</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 8S * 24V * 20А – <b>1200 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 8S * 24V * 40А – <b>1500 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 8S * 24V * 60А – <b>2200 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 8S * 24V * 80А – <b>3100 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 8S * 24V * 100А – <b>4100 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 8S * 24V * 150А – <b>6600 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 8S * 24V * 200А – <b>10200 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 8S * 24V * 250А – <b>10900 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 8S * 24V * 60А – <b>4100 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 8S * 24V * 100А – <b>5700 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 8S * 24V * 150А – <b>7800 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 8S * 24V * 200А – <b>10600 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 8S * 24V * 250А – <b>11400 р.</b>\n' +
				'Плата Dаly ВМS (К-тип смарт): LiFеРО4 * 8S * 24V * 60А – <b>4500 р.</b>\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ 
								{'text': '↩', 'callback_data': self.ucode + 'stock'},
								{'text': '12B', 'callback_data': self.ucode + 'v12'}, 
								{'text': '36B', 'callback_data': self.ucode + 'v36'}, 
								{'text': '48B', 'callback_data': self.ucode + 'v48'}, 
								{'text': '60B', 'callback_data': self.ucode + 'v60'}, 
							],
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def v36(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' +
				quote('⚡️⚡️⚡️ Плaтa BMS ⚡️⚡️⚡️\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'✅ В НАЛИЧИИ:\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'<b>Платы на 36В аккумуляторы (12S, 43.8V):</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 12S * 36V * 20А – <b>1200 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 12S * 36V * 40А – <b>2200 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 12S * 36V * 60А – <b>2900 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 12S * 36V * 80А – <b>4300 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 12S * 36V * 100А – <b>5400 р.</b>\n' +
				'Плата Dаly ВМS (К-тип смарт): LiFеРО4 * 12S * 36V * 60А – <b>5000 р.</b>\n' +
				'Плата Dаly ВМS (К-тип смарт): LiFеРО4 * 12S * 36V * 100А – <b>6200 р.</b>\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ 
								{'text': '↩', 'callback_data': self.ucode + 'stock'},
								{'text': '12B', 'callback_data': self.ucode + 'v12'}, 
								{'text': '24B', 'callback_data': self.ucode + 'v24'}, 
								{'text': '48B', 'callback_data': self.ucode + 'v48'}, 
								{'text': '60B', 'callback_data': self.ucode + 'v60'}, 
							],
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def v48(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' + quote(
				'⚡️⚡️⚡️ Плaтa BMS ⚡️⚡️⚡️\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'✅ В НАЛИЧИИ:\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'<b>Платы на 48В аккумуляторы (16S, 58.4V):</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 16S * 48V * 20А – <b>1600 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 16S * 48V * 40А – <b>2200 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 16S * 48V * 60А – <b>3000 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 16S * 48V * 80А – <b>4700 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 16S * 48V * 100А – <b>5100 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 16S * 48V * 150А – <b>7800 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 16S * 48V * 200А – <b>12000 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 16S * 48V * 100А – <b>6500 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 16S * 48V * 150А – <b>9400 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 16S * 48V * 200А – <b>12100 р.</b>\n' +
				'Плата Dаly ВМS (К-тип смарт): LiFеРО4 * 16S * 48V * 100А – <b>6800 р.</b>\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ 
								{'text': '↩', 'callback_data': self.ucode + 'stock'},
								{'text': '12B', 'callback_data': self.ucode + 'v12'}, 
								{'text': '24B', 'callback_data': self.ucode + 'v24'}, 
								{'text': '36B', 'callback_data': self.ucode + 'v36'}, 
								{'text': '60B', 'callback_data': self.ucode + 'v60'}, 
							],
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def v60(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' +
				quote('⚡️⚡️⚡️ Плaтa BMS ⚡️⚡️⚡️\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'✅ В НАЛИЧИИ:\n' +
				'\n' +
				'********************************************\n' +
				'\n' +
				'<b>Платы на 60В аккумуляторы (20S, 73.0V):</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 20S * 60V * 20А – <b>2300 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 20S * 60V * 40А – <b>2500 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 20S * 60V * 60А – <b>3200 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 20S * 60V * 80А – <b>5000 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 20S * 60V * 100А – <b>5400 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 20S * 60V * 150А – <b>8100 р.</b>\n' +
				'Плата ВМS (Dаly): LiFеРО4 * 20S * 60V * 200А – <b>12300 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 20S * 60V * 100А – <b>7900 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 20S * 60V * 150А – <b>9100 р.</b>\n' +
				'Плата smаrt ВМS (Dаly): LiFеРО4 * 20S * 60V * 200А – <b>12600 р.</b>\n' +
				'Плата Dаly ВМS (К-тип смарт): LiFеРО4 * 20S * 60V * 100А – <b>7900 р.</b>\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ 
								{'text': '↩', 'callback_data': self.ucode + 'stock'},
								{'text': '12B', 'callback_data': self.ucode + 'v12'}, 
								{'text': '24B', 'callback_data': self.ucode + 'v24'}, 
								{'text': '36B', 'callback_data': self.ucode + 'v36'}, 
								{'text': '48B', 'callback_data': self.ucode + 'v48'}, 
							],
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))