from Articles.LifePO4 import LifePO4
from Articles.YZPower import YZPower
from Articles.BMSDaly import BMSDaly

class Catalog:
	async def init (self, Query):
		await LifePO4().init(Query)
		await BMSDaly().init(Query)
		await YZPower().init(Query)