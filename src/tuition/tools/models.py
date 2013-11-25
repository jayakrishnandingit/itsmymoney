'''
Created on Feb 6, 2013

@author: jayakrishnan
'''
from google.appengine.ext import db
from tuition.common.models import CommonModel

class Expenses(CommonModel):
    user = db.ReferenceProperty(required = True)
    type = db.StringProperty(required = True)
    # Any change in BELOW TWO properties must be handled in js too.
    amount = db.FloatProperty(default = 0.0, required = True)
    dateOfExpense = db.DateProperty(required = True)
    comments = db.TextProperty()
    createdOn = db.DateTimeProperty(auto_now_add=True)
    updatedOn = db.DateTimeProperty(auto_now=True)

class Debt(CommonModel):
	user = db.ReferenceProperty(required = True)
	type = db.StringProperty(required = True)
	# Any change in BELOW TWO properties must be handled in js too.
	amount = db.FloatProperty(default = 0.0, required = True)
	incurredDate = db.DateProperty(required = True)
	returnDate = db.DateProperty(required = True)
	markedOnCalendar = db.DateProperty()
	hasReturned = db.BooleanProperty(default=False)
	expenseOfMonth = db.DateProperty()
	comments = db.TextProperty()
	createdOn = db.DateTimeProperty(auto_now_add=True)
	updatedOn = db.DateTimeProperty(auto_now=True)

	@property
	def calendarReminderURL(self):
		from tuition.urlPatterns import UrlPattern
		from tuition.utils.utils import URLCreator

		return '%s?key=%s' % (URLCreator(UrlPattern.VIEW_DEBTS), str(self.key()))