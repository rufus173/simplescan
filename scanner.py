import sane
# python-sane wrapper
class SaneScanner():
	def __init__(self,device_name):
		self.scanner = sane.open(device_name)
		
