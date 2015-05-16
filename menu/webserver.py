from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			#Looks for url with /hello
			if self.path.endswith("/hello"):
				#Succcesful get request
				self.send_response(200)
				#Indicate replying with text as html
				self.send_header('Content-type', 'text/html')
				#Indicates end of http headers
				self.end_headers()
				
				output = ""
				output += "<html><body>Hello!</body></html>"
				#Send a message back to oclient
				self.wfile.write(output)
				print output
				return
				
		except:
			self.send_error(404, "File Not Found %s" % self.path)
		

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
		
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

















if __name__ == '__main__':
	main()