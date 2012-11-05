import webapp2
import json
from google.appengine.ext import db


class SBRecipe(db.Model):
    author = db.UserProperty()
    comments = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    xml = db.TextProperty()
    brewer = db.StringProperty()
    name = db.StringProperty()
    style = db.StringProperty()
    
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, webapp2 World!')
        
class RecipeHandler(webapp2.RequestHandler):
    def get(self,name=None):
        if name is None or name == '':
            name = 'no one'
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello , *' + name + '*!')
        
    def post(self):
        #Load the JSON values that were sent to the server
        #dictionary = json.loads(self.request.body)
        self.response.write('Hello , *' + self.request.body + '*!')
        

app = webapp2.WSGIApplication([('/', MainPage),
                               (r'/recipes/(.*)', RecipeHandler)], debug=True)