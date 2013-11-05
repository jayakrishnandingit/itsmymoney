'''
Created on Jan 4, 2013

@author: jayakrishnan
'''
from google.appengine.ext import db

class Role(db.Model):
    name = db.StringProperty(required = True)
    permissions = db.StringListProperty(default = [])
