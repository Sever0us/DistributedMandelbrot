from tools import rate_limited
import requests
import json
import numpy as np

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

        max_iterations = 100
        for n in range(max_iterations):
            if abs(z) > 2:
                return n/max_iterations
            z = z*z + c

        return 0

    def submit_response(self, jobs):
        requests.post(self.address+'/api/submit_result', data=json.dumps(jobs).encode())


    def get_image_resolution(self):
        response = requests.get(self.address+'/api/get_image_resolution')
        return int(response.text)

    @rate_limited
    def get_image_data(self):
        response = requests.get(self.address+'/api/get_image_data')
        
        if response.text == 'wait':
            return False
        else:
            return json.loads(response.text)

    def get_image(self):
        resolution = self.get_image_resolution()
        while True:
            pixel_list = self.get_image_data()
            if pixel_list:
            	break

        return np.reshape(pixel_list, (-1, resolution))
        
