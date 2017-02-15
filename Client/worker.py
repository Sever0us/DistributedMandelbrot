from tools import rate_limited
import requests
import json

class worker:
	def __init__(self, address):
		self.address = address

	@rate_limited
	def get_job(self):
		response = requests.get(self.address+'/api/get_job')
		data = json.loads(response.text)
		
		calculated_value = self.compute(data['x'], data['y'])

		print(calculated_value)

	def compute(self, x, y):
		z = complex(x, y)
		c = complex(x, y)

		for n in range(100):
			if abs(z) > 2:
				return n
			z = z*z + c

		return 0