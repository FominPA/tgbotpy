import asyncio, aiohttp
import json
from sets import botdata
from Articles.Article import Article
from urllib.parse import quote

class YZPower(Article):
	ucode = '1285650'

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
				if 'spec' in Query['callback_query']['data']:
					await self.spec(Query)

	def get_photo(self): return 'https://titanat.ru/wp-content/uploads/2019/10/photo_2023-04-05_12-59-20-e1681214024292-300x300.jpg'

	def get_general_text(self): 
		return ('&caption=' +
			quote('YZРоwеr зарядка LiFеРО4') +
			'&parse_mode=html' +
			'&reply_markup=' +
			json.dumps({
				'inline_keyboard': 
					[[{'text': 'Подробнее', 'callback_data': self.ucode + 'more'},],]
			}))

	async def more(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' + quote(
				'YZРоwеr зарядка LiFеРО4\n' +
				'___________________________\n' +
				'\n' +
				'Перeд закaзом обязательно (!!!) уточните в cоoбщении или по телефону наличиe конкрeтнoй мoдификaции зaрядного уcтрoйcтва.\n' +
				'\n' +
				'Заpядныe уcтройcтвa YZPower провeрены временeм и практикой, показали сeбя исключительно с пoлoжитeльной cтoроны, стaбильно рабoтают дaжe в тяжелыx, не pекомeндовaнныx условиях (высокая влажность и сильные вибрации / тряска).\n' +
				'\n' +
				'Данные устройства будучи НЕ влагозащищенными НЕ рекомендуется устанавливать стационарно в агрессивные среды с повышенной влажностью, однако они успешно прошли испытание более чем 2х летней эксплуатации при стационарной установке в спортивной рыболовной лодке и интенсивной эксплуатации в режиме соревнований.\n' +
				'\n' +
				'Производитель данных зарядных устройств имеет многолетний опыт работы и подавляющее большинство положительных отзывов о своем продукте.\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
							[ {'text': 'Технические характеристики', 'callback_data': self.ucode + 'spec'}, ],
							[ {'text': 'Наличие и цены', 'callback_data': self.ucode + 'stock'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def stock(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' + quote(
				'YZРоwеr зарядка LiFеРО4\n' +
				'___________________________\n' +
				'\n' +
				'В наличии:\n' +
				'YZРоwеr зарядка LiFеРО4 АКБ: 14.6V * 10А - 2200 руб.\n' +
				'YZРоwеr зарядка LiFеРО4 АКБ: 14.6V * 20А - 4500 руб.\n' +
				'YZРоwеr зарядка LiFеРО4 АКБ: 29.2V * 10А – 4500 руб.\n' +
				'YZРоwеr зарядка LiFеРО4 АКБ: 29.2V * 20А - 6600 руб.\n' +
				'YZРоwеr зарядка LiFеРО4 АКБ: 43.8V * 10А – 6600 руб.\n' +
				'YZРоwеr зарядка LiFеРО4 АКБ: 43.8V * 20А – 10400 руб.\n' +
				'\n' +
				'Под заказ доступны зарядные устройства почти на любой вольтаж и силу тока – звоните / пишите.\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
							[ {'text': 'Подробнее', 'callback_data': self.ucode + 'more'}, ],
							[ {'text': 'Технические характеристики', 'callback_data': self.ucode + 'spec'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))

	async def spec(self, Query):
		async with aiohttp.ClientSession() as session:
			await session.get(botdata.BASE_URL + 'editMessagecaption?caption=' + quote(
				'YZРоwеr зарядка LiFеРО4\n' +
				'___________________________\n' +
				'\n' +
				'Характеристики:\n' +
				'Назначение: зарядка LiFеРО4 аккумуляторов.\n' +
				'Максимальный ток заряда: 10-20 А (см. модификацию)\n' +
				'Разъемы / клеммы: входной – евро вилка; выходной – зажимы типа «крокодил»\n' +
				'Материал: Алюминиевый корпус\n' +
				'Режим работы зарядного устройства: СС (постоянный ток) / СV (постоянное напряжение)\n' +
				'Рабочая температура: -20 ~ 60 градусов\n' +
				'Температура хранения: -40 ~ + 80 градусов\n' +
				'Влажность при эксплуатации: 20 ~ 90% относительной влажности\n' +
				'Функции защиты: от перенапряжения / перегрева / перегрузки по току / короткого замыкания и полярности\n' +
				'Индикатор светодиода: красный - зарядка, зеленый - зарядка завершена или подготовка к зарядке.\n') +
				'&parse_mode=html' +
				'&reply_markup=' +
				json.dumps({
					'inline_keyboard': 
						[
							[ {'text': 'Свернуть', 'callback_data': self.ucode + 'general'}, ],
							[ {'text': 'Подробнее', 'callback_data': self.ucode + 'more'}, ],
							[ {'text': 'Наличие и цены', 'callback_data': self.ucode + 'stock'}, ],
						]
					}) +
				'&chat_id=' + str(Query['callback_query']['message']['chat']['id']) +
				'&message_id=' + str(Query['callback_query']['message']['message_id']))