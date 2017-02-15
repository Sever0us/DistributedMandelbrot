from tools import rate_limited
import requests

class worker:
	def __init__(self, address):
		self.address = address
		self.UID = self.register()

	@rate_limited
	def register(self):
		response = requests.get(self.address+'/api/register')
		print('Cool! I am ' + response.text)
		return response.text

	@rate_limited
	def get_job(self):
		response = requests.get(self.address+'/api/get_job')
