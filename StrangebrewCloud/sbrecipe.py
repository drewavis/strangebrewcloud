import re
from xml.dom import minidom
from google.appengine.ext import db

class SBRecipe(db.Model):
    comments = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    xml = db.TextProperty()
    brewer = db.StringProperty()
    name = db.StringProperty()
    style = db.StringProperty()

class RecipeData():
    def __init__(self, xml):
    
        r = re.compile('<\?xml:stylesheet[^>]*>')
        xml = r.sub('', xml)
        xmldoc = minidom.parseString(xml.encode('latin1'))
        self.og = xmldoc.getElementsByTagName('OG')[0].firstChild.data.strip()
        self.fg = xmldoc.getElementsByTagName('FG')[0].firstChild.data.strip()
        self.size = xmldoc.getElementsByTagName('SIZE')[0].firstChild.data.strip() 
        self.size += " " + xmldoc.getElementsByTagName('SIZE_UNITS')[0].firstChild.data.strip()
        malts = xmldoc.getElementsByTagName('FERMENTABLES')[0].getElementsByTagName('ITEM')        
        self.malts = []
        for item in malts :
            self.malts.append(item.getElementsByTagName('AMOUNT')[0].firstChild.data.strip() + " " +
                              item.getElementsByTagName('UNITS')[0].firstChild.data.strip() + " " +
                              item.getElementsByTagName('MALT')[0].firstChild.data.strip())
        
        hops = xmldoc.getElementsByTagName('HOPS')[0].getElementsByTagName('ITEM')        
        self.hops = []
        for item in hops :
            self.hops.append(item.getElementsByTagName('AMOUNT')[0].firstChild.data.strip() + " " +
                              item.getElementsByTagName('UNITS')[0].firstChild.data.strip() + " " +
                              item.getElementsByTagName('HOP')[0].firstChild.data.strip() + " (" +
                              item.getElementsByTagName('TIME')[0].firstChild.data.strip() + " min)" )    