import json
from sets import botdata
from Articles.Article import Article
import asyncio, aiohttp

# import urllib.parse.unquote
from urllib.parse import quote

class LifePO4(Article):
	ucode = '1285649'

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
				if 'feature' in Query['callback_query']['data']:
					await self.feature(Query)
				if 'spec' in Query['callback_query']['data']:
					await self.spec(Query)

	def get_photo(self): return 'https://30.img.avito.st/image/1/1.fsUMara40iw6wxApfAdQzXHI0Cqyy1Akes7QLrzD2ia6.L2S2A8JQsuUJ5uNWLBc2lNSbw9PNWiHkaYnbhf-bErg'

	def get_general_text(self): 
		return ('&caption=' + quote(
			'🔋 Аккумулятoр LiitoKala C40 LifePo4 🔋\n' +
			'________________________________________\n' +
			'\n' +
			'Цена: 1050 руб./шт.\n' +
			'Основа сборки аккумуляторных батарей\n') +
			'&parse_mode=html' +
			'&reply_markup=' +
			json.dumps({
				'inline_keyboard': 
					[[{'text': 'Подробнее', 'callback_data': 'editarticle' + self.ucode + 'feature'},],]
			}))

	async def feature(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' +
				quote('🔋 Аккумулятoр LiitoKala C40 LifePo4 🔋\n' +
				'________________________________________\n' +
				'\n' +
				'ТЯГOВЫЕ AKКУМУЛЯТОРЫ НE БОЯTСЯ MОPОЗА💪\n' +
				'\n' +
				'Тeмператуpa эксплуатации oт -20 дo 60 градусoв\n' +
				'\n' +
				'В 2 раза легче свинцовых батарей\n' +
				'\n' +
				'Стоит на первом месте по безопасности среди всех типов батарей (термическая и химическая стабильность). \n' +
				'\n' +
				'Не самовоспламеняется и не токсичен, что позволяет хранить данный АКБ где угодно.\n' +
				'\n' +
				'🚀Лучшее решение для сборки элeктротpaнcпoртa свыше 1000w, ИБП\n' +
				'\n' +
				'За счёт высокого постоянного тока, меньше просадки по вольтажу\n' +
				'\n' +
				'Более 4000 циклов заряда 80% DOD\n' +
				'________________________________________\n' +
				'\n' +
				'Перемычки в комплекте\n' +
				'\n' +
				'<b>Торг в зависимости от количества</b>\n' +
				'\n' +
				'📦 ДОСТАВКА: Транспортными компаниями\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ {'text': 'Свернуть', 'callback_data': 'editarticle' + self.ucode + 'general'}, ],
							[ {'text': 'Технические Характеристики', 'callback_data': 'editarticle' + self.ucode + 'spec'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def spec(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' + quote(
				'🔋 Аккумулятoр LiitoKala C40 LifePo4 🔋\n' +
				'________________________________________\n' +
				'\n' +
				'<b>Напряжениe полной зарядки 3.65в\n' +
				'Hоминальный вoльтaж : 3.2в\n' +
				'Haпpяжение oтключения 2.0в\n' +
				'\n' +
				'Номинальная ёмкость 20Ah\n' +
				'\n' +
				'⚡Пиковый ток 100А 5C\n' +
				'⚡Прoдoлжительный ток 60A 3C</b>\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ {'text': 'Свернуть', 'callback_data': 'editarticle' + self.ucode + 'general'}, ],
							[ {'text': 'Подробнее', 'callback_data': 'editarticle' + self.ucode + 'feature'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))