from Articles.LifePO4 import LifePO4
from Articles.YZPower import YZPower
from Articles.BMSDaly import BMSDaly

class Catalog:
	def __init__ (self, Query):
		LifePO4(Query)
		BMSDaly(Query)
		YZPower(Query)