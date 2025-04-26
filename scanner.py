import sane
from PIL import Image
# python-sane wrapper
class SaneScanner():
	def __init__(self,device_name):
		self.scanner = sane.open(device_name)
	def scan(self):
		return self.scanner.scan()	
