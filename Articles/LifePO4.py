from requests import get
import json
from sets import botdata

class LifePO4:
	ucode = '1285649'
	def __init__ (self, Query):
		if 'message' in Query:
			if Query['message']['text'] == 'Каталог':
				self.send(Query)
				return
		elif 'callback_query' in Query:
			if self.ucode in Query['callback_query']['data']:
				if 'general' in Query['callback_query']['data']:
					self.back_to_general(Query)
					return
				if 'feature' in Query['callback_query']['data']:
					self.feature(Query)
					return
				if 'spec' in Query['callback_query']['data']:
					self.spec(Query)
					return

	def get_photo(self): return 'https://30.img.avito.st/image/1/1.fsUMara40iw6wxApfAdQzXHI0Cqyy1Akes7QLrzD2ia6.L2S2A8JQsuUJ5uNWLBc2lNSbw9PNWiHkaYnbhf-bErg'

	def get_general_text(self): 
		return ('&caption=' +
			'🔋 Аккумулятoр LiitoKala C40 LifePo4 🔋\n' +
			'________________________________________\n' +
			'\n' +
			'Цена: 1050 руб./шт.\n' +
			'Основа сборки аккумуляторных батарей\n' +
			'&parse_mode=html' +
			'&reply_markup=' +
			json.dumps({
				'inline_keyboard': 
					[[{'text': 'Подробнее', 'callback_data': self.ucode + 'feature'},],]
			}))

	def send(self, Query):
		get(botdata.BASE_URL + 'sendphoto?chat_id=' + botdata.MY_ID + 
			'&photo=' + self.get_photo() + self.get_general_text()
		)

	def back_to_general(self, Query):
		get(botdata.BASE_URL + 'editMessagecaption?' +
			self.get_general_text() +
			'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
			'&message_id=' + str(Query['callback_query']['message']['message_id'])
		)

	def feature(self, Query):
		get(botdata.BASE_URL + 'editMessagecaption?caption=' +
			'🔋 Аккумулятoр LiitoKala C40 LifePo4 🔋\n' +
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
			'📦 ДОСТАВКА: Транспортными компаниями\n' +
			'&parse_mode=html' +
			'&reply_markup=' +
			json.dumps({
				'inline_keyboard': 
					[
						[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
						[ {'text': 'Технические Характеристики', 'callback_data': self.ucode + 'spec'}, ],
					]
				}) +
			'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
			'&message_id=' + str(Query['callback_query']['message']['message_id'])
		)

	def spec(self, Query):
		print(get(botdata.BASE_URL + 'editMessagecaption?caption=' +
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
			'⚡Прoдoлжительный ток 60A 3C</b>\n' +
			'&parse_mode=html' +
			'&reply_markup=' +
			json.dumps({
				'inline_keyboard': 
					[
						[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
						[ {'text': 'Подробнее', 'callback_data': self.ucode + 'feature'}, ],
					]
				}) +
			'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
			'&message_id=' + str(Query['callback_query']['message']['message_id'])
		).json())