import http.server
import socketserver
import secrets
import queue
import numpy as np
import json
from itertools import product
import pickle

PORT = 80
resolution = 100

# Create jobs
cx, cy, r =  -0.74529, 0.113075, 1.5E-4
x = np.linspace(cx-r, cx+r, resolution)
y = np.linspace(cy-r, cy+r, resolution)
jobs = product(x, y)
counter = 0
finished = 0

results = [None for i in range(resolution**2)]

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/api/get_job':
            self.get_job()
        elif self.path == '/api/get_image_data':
            self.get_image_data()
        elif self.path == '/api/get_image_resolution':
            self.get_image_resolution()
        else:
            self.error404()

    def do_POST(self):
        if  self.path == '/api/submit_result':
            self.submit_result()
        else:
            self.error404()

    def get_job(self):
        global jobs
        global counter 

        # Get a job and assign a unique job number 
        response = {}
        for i in range(1000):
            try:
                job = jobs.__next__()
                response[counter] = {'x':job[0], 'y':job[1]}
                counter += 1 
            except StopIteration:
                break
            
        if response == {}:  
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write('done'.encode())
        else: 
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

    def submit_result(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        complete_jobs = json.loads(post_data.decode())

        global results
        global finished

        for job_number in complete_jobs:
            results[int(job_number)] = complete_jobs[job_number]
            finished += 1

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('received'.encode())

    def get_image_resolution(self):
        global resolution

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(str(resolution).encode())
        
    def get_image_data(self):
        global results
        global resolution
        global finished

        if finished == resolution**2:
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(pickle.dumps(results))
        else:
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write('wait'.encode())

    def error404(self):
        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>404 Error</title></head>'.encode())
        self.wfile.write('<body><h1>404 Not found</h1></body></html>'.encode())


with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("serving at port", PORT)
    httpd.serve_forever()
