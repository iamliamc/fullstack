from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, re

## import CRUD operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
## create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/edit"):
                dbID = re.sub("\D", "", str(self.path))
                r_name = session.query(Restaurant).filter_by(id = dbID).one()
                if r_name != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html></body>"
                    output += "<h2> %s </h2>" % r_name.name
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>''' % dbID
                    output += '''<input name="rename" type="text" ><input type="submit" value="rename" placeholder = "%s"> </form>''' % r_name.name
                    output += "</html></body>"
                    self.wfile.write(output)
            
            if self.path.endswith("/delete"):
                dbID = re.sub("\D", "", str(self.path))
                r_delete = session.query(Restaurant).filter_by(id = dbID).one()
                print r_delete.name
                if r_delete != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Do you want to delete %s</h2>" % r_delete.name
                    output += "<h2> %s </h2>" % r_delete.name
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'><input type="submit" value="delete"></form>''' %dbID
                    output += "</html></body>"
                    self.wfile.write(output)        
                
                
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>What Restaurant would you like to create?</h2><input name="newRestaurant" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "<h2></h2>"
                output += "</body></html>"
                self.wfile.write(output)
                
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ""
                output += "<a href = '/restaurants/new'> Make new Restaurant Here </a></br></br>"
                output += "<html><body>"
                for restaurant in restaurants:
                    rID = restaurant.id
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % rID
                    output += "</br>"
                    output += "<a href='restaurants/%s/delete'>Delete</a>" % rID
                    output += "</br>"
                    output += "</br>"
                output += "</html></body>"
                self.wfile.write(output)
                return
                
                
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    newRestaurant = fields.get('newRestaurant')
                    myNewRestaurant = Restaurant(name = str(newRestaurant[0]))
                    session.add(myNewRestaurant)
                    session.commit()                    
                
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    
            elif self.path.endswith("/hello"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                
            elif self.path.endswith("/edit"):
                dbID = re.sub("\D", "", str(self.path))
                r_name = session.query(Restaurant).filter_by(id = dbID).one()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('rename')
                    print messagecontent
                r_name.name = messagecontent[0]
                session.add(r_name)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            
            elif self.path.endswith("/delete"):
                dbID = re.sub("\D", "", str(self.path))
                r_delete = session.query(Restaurant).filter_by(id = dbID).one()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if r_delete != []:
                    session.delete(r_delete)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
