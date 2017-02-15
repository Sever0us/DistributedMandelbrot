import http.server
import socketserver
import secrets
import queue
import numpy as np
import json
from itertools import product

PORT = 80
resolution = 100

# Create jobs
cx, cy, r =  -0.74529, 0.113075, 1.5E-4
x = np.linspace(cx-r, cx+r, resolution)
y = np.linspace(xy-r, cy+r, resolution)
jobs = product(x, y)
counter = 0

results = [None for i in range(resolution**2)]

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/api/get_job':
            self.get_job()
        else:
            self.error404()

    def do_POST(self):
        if self.path == '/api/submit_result':
            self.submit_result()
        else:
            self.error404()

    def get_job(self):
        global jobs
        global counter 

        # Get a job and assign a unique job number 
        try:
            job = jobs.next()
            job_number = counter
            counter += 1 

            response = {'job_number':job_number,
                        'x':job[0],
                        'y':job[1]}

            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(json.dumps(response))


        except StopIteration:
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write('done'.encode())

    def error404(self):
        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>404 Error</title></head>'.encode())
        self.wfile.write('<body><h1>404 Not found</h1></body></html>'.encode())


with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("serving at port", PORT)
    httpd.serve_forever()
