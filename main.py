from Listener import Listener
from sets.serverdata import con
from sets import botdata
import Articles.Article
import buttons
import asyncio, aiohttp

Listener(con)

# Запускаем слушатель
# 	Слушает запросы до тех пор пока не появится новая пачка
# 	Отделяет пачку
# 	Передает ёё парсеру
# 		...
# 		Принимает пачку запросов
# 		Разделяет их на пользователей
# 		Для каждого пользователя запускает последовательный поток
# 		А мог бы для каждого пользователя создавать поток и запускать его
# 		...
# 	Запоминает id последнего нового запроса