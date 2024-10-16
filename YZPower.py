from requests import get
import json
import botdata

class YZPower:
	ucode = '1285650'

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
				if 'more' in Query['callback_query']['data']:
					self.more(Query)
					return
				if 'stock' in Query['callback_query']['data']:
					self.stock(Query)
					return
				if 'spec' in Query['callback_query']['data']:
					self.spec(Query)
					return

	def get_photo(self): return 'https://titanat.ru/wp-content/uploads/2019/10/photo_2023-04-05_12-59-20-e1681214024292-300x300.jpg'

	def get_general_text(self): 
		return ('&caption=' +
			'YZРоwеr зарядка LiFеРО4' +
			'&parse_mode=html' +
			'&reply_markup=' +
			json.dumps({
				'inline_keyboard': 
					[[{'text': 'Подробнее', 'callback_data': self.ucode + 'more'},],]
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

	def more(self, Query):
		print(get(botdata.BASE_URL + 'editMessagecaption?caption=' +
			'YZРоwеr зарядка LiFеРО4\n' +
			'___________________________\n' +
			'\n' +
			'Перeд закaзом обязательно (!!!) уточните в cоoбщении или по телефону наличиe конкрeтнoй мoдификaции зaрядного уcтрoйcтва.\n' +
			'\n' +
			'Заpядныe уcтройcтвa YZPower провeрены временeм и практикой, показали сeбя исключительно с пoлoжитeльной cтoроны, стaбильно рабoтают дaжe в тяжелыx, не pекомeндовaнныx условиях (высокая влажность и сильные вибрации / тряска).\n' +
			'\n' +
			'Данные устройства будучи НЕ влагозащищенными НЕ рекомендуется устанавливать стационарно в агрессивные среды с повышенной влажностью, однако они успешно прошли испытание более чем 2х летней эксплуатации при стационарной установке в спортивной рыболовной лодке и интенсивной эксплуатации в режиме соревнований.\n' +
			'\n' +
			'Производитель данных зарядных устройств имеет многолетний опыт работы и подавляющее большинство положительных отзывов о своем продукте.\n' +
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
			'&message_id=' + str(Query['callback_query']['message']['message_id'])
		).json())

	def stock(self, Query):
		print(get(botdata.BASE_URL + 'editMessagecaption?caption=' +
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
			'Под заказ доступны зарядные устройства почти на любой вольтаж и силу тока – звоните / пишите.\n' +
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
			'&message_id=' + str(Query['callback_query']['message']['message_id'])
		).json())

	def spec(self, Query):
		print(get(botdata.BASE_URL + 'editMessagecaption?caption=' +
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
			'Индикатор светодиода: красный - зарядка, зеленый - зарядка завершена или подготовка к зарядке.\n' +
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
			'&message_id=' + str(Query['callback_query']['message']['message_id'])
		).json())