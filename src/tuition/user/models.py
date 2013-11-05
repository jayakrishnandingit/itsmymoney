'''
Created on Jul 18, 2013

@author: jayakrishnan
'''

from google.appengine.ext import db
from tuition.common.models import CommonModel

class User(CommonModel):
    firstName = db.StringProperty(required=True)
    lastName = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    alternateEmail = db.EmailProperty(required=True)
    dob = db.DateProperty(required=True)
    about = db.TextProperty()
    createdOn = db.DateTimeProperty(auto_now_add=True)
    updatedOn = db.DateTimeProperty(auto_now=True)

    @property
    def name(self):
    	return '%s %s' % (self.firstName, self.lastName)
