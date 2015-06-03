from data import data_pb2 as pb
from data import config


class DataHandler():
	dataset = pb.DataBase()

	try:
		with open(config.current_datafile, 'rb') as f:
			dataset.ParseFromString(f.read())
	except IOError:
		print "Could not load data, creating new file at " + config.current_datafile

	def newRun(self):
		""" Initialize a new run. Any old run will be saved."""
		self.run = self.dataset.run.add()

	def addArgs(self, args):
		""" Expects args to be a dictionary of var-value pairs.
			Overwrites earlier changes to the same var.
			Make sure all data is in the right type (convert enums!)."""
		for var in args:
			if var=='runid':
				self.run.runid = args[var]
			elif var=='i':
				self.run.i = args[var]
			elif var=='ID':
				self.run.ID = args[var]
			elif var=='Agent':
				self.run.Agent = args[var]
			elif var=='Language':
				self.run.Language = args[var]
			elif var=='Age':
				self.run.Age = args[var]
			elif var=='Referer':
				self.run.Referer = args[var]
			elif var=='header':
				self.run.header = args[var]
			elif var=='adtype':
				self.run.adtype = args[var]
			elif var=='color':
				self.run.color = args[var]
			elif var=='productid':
				self.run.productid = args[var]
			elif var=='price':
				self.run.price = args[var]
		
	enum = {
		'agent': {
			'osx'    : self.dataset.run.OSX,
			'windows': self.dataset.run.Windows,
			'linux'  : self.dataset.run.Linux,
			'mobile' : self.dataset.run.Mobile
		},
		'language': {
			'EN': self.dataset.run.EN,
			'NL': self.dataset.run.NL,
			'GE': self.dataset.run.GE,
			'NA': self.dataset.run.NA
		},
		'referer': {
			'google': self.dataset.run.Google,
			'bing'  : self.dataset.run.Bing,
			'na'    : self.dataset.run.NO
		},
		'header': {
			'5' : self.dataset.run.FIVE,
			5   : self.dataset.run.FIVE,
			'15': self.dataset.run.FIFTEEN,
			15  : self.dataset.run.FIFTEEN,
			'35': self.dataset.run.THIRTFIVE,
			35  : self.dataset.run.THIRTFIVE
		},
		'adtype': {
			'skyscraper': self.dataset.run.skyscraper,
			'square'    : self.dataset.run.square,
			'banner'    : self.dataset.run.banner
		},
		'color': {
			'black': self.dataset.run.black
			'blue' : self.dataset.run.blue
			'green': self.dataset.run.green
			'red'  : self.dataset.run.red
			'white': self.dataset.run.white
		}
	}
	def convertEnum(self, etype, v):
		return self.enum[etype][v]

	def writeAway(self):
		with open(config.current_datafile, 'wb') as f:
			f.write(self.dataset.SerializeToString())
