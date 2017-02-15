from tools import rate_limited
import requests
import json

class worker:
    def __init__(self, address):
        self.address = address
        self.counter = 0

    @rate_limited
    def get_job(self):
        print('Get jobs')
        response = requests.get(self.address+'/api/get_job')
        if response.text == 'done':
            return False
        data = json.loads(response.text)

        print('Calculate')
        calculated_values = {}
        for job_number in data:
            r = self.compute(data[job_number]['x'], data[job_number]['y'])
            calculated_values[job_number] = r
            self.counter += 1
    

        print('Post results')
        self.submit_response(calculated_values)

        return True

    def compute(self, x, y):
        z = complex(x, y)
        c = complex(x, y)

        for n in range(100):
            if abs(z) > 2:
                return n
            z = z*z + c

        return 0

    def submit_response(self, jobs):
        requests.post(self.address+'/api/submit_result', data=json.dumps(jobs).encode())
