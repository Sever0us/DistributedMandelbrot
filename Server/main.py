import http.server
import socketserver
import secrets

PORT = 80
global worker_tokens = set()

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
         if self.path == '/api/register':
             self.register()
         else:
         	self.error404()
        return

    def register(self):
    	# Create new token and add to list of workers
        new_token = secrets.token_hex(32)

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(new_token)

        global worker_tokens
        worker_tokens.add(new_token)

    def error404(self):
        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>404 Error</title></head>')
        self.wfile.write('<body><h1>404 Not found</h1></body></html>')


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()