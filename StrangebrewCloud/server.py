import webapp2
from xml.dom import minidom
from sbrecipe import SBRecipe

   
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, webapp2 World!')
        
class RecipeHandler(webapp2.RequestHandler):
    def get(self,name=None):        
        # return all recipes w/ id's:
        if name is None or name == '' or name == 'all':
            resp='<xml>'
            recipes_query = SBRecipe.all()
            for recipe in recipes_query:
                resp += '<recipe id=\''+str(recipe.key().id()) + '\' name=\'' + recipe.name \
                    + '\' style=\'' + recipe.style + '\' />'
            resp += '</xml>'  
            
            self.response.headers['Content-Type'] = 'application/xml'   
            self.response.write(resp)
            return     
            
        else:
            # try to get ID
            try:
                r_id = int(name)
                recipe = SBRecipe.get_by_id(r_id)
                self.response.headers['Content-Type'] = 'application/xml'   
                self.response.write(recipe.xml)
                return 
               
               
            except:
                self.error(400)
                self.response.out.write('Bad id.')      
                return
           
       
    def post(self, name=None):       
        
        # first get the xml:
        xmltxt = self.request.body
        
        # is it good?
        try: 
            xmldoc = minidom.parseString(xmltxt.encode('ISO-8859-1'))  
        except:
            self.error(400)
            self.response.out.write('WTF? That is some bad xml, Poncho. \nPlease try again.')      
            return
    
        if xmldoc.getElementsByTagName('STRANGEBREWRECIPE') == [] :
            self.error(400)
            self.response.out.write('That just doesn\'t look like a StrangeBrew Recipe to me.  Sorry.')      
            return
        
        # create new recipe object
        recipe = SBRecipe()
        recipe.xml = xmltxt;
        recipe.version = xmldoc.getElementsByTagName('STRANGEBREWRECIPE')[0].attributes['version'].value
        recipe.brewer = xmldoc.getElementsByTagName('BREWER')[0].firstChild.data.strip()
        recipe.name = xmldoc.getElementsByTagName('NAME')[0].firstChild.data.strip()
        recipe.style = xmldoc.getElementsByTagName('STYLE')[0].firstChild.data.strip()
        if xmldoc.getElementsByTagName('NOTES')[0].firstChild != None :
            recipe.comments = xmldoc.getElementsByTagName('NOTES')[0].firstChild.data.strip()
        
        # does this already exist?
        if SBRecipe.all().filter("name =", recipe.name).count(limit=10) > 0 :
            self.error(400)
            self.response.out.write('A recipe with that name already exists.')
        else :
            k = recipe.put()       
            self.response.write('recipe id: ' + str(k.id()))
        

app = webapp2.WSGIApplication([('/', MainPage),
                               (r'/recipes/(.*)', RecipeHandler)], debug=True)