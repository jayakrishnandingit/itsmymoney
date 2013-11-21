BASIC_TYPES = (int, long, float, bool, dict, basestring, list)

import datetime
from google.appengine.ext import db
from django.utils.datastructures import SortedDict

class CommonModel(db.Model):
	maxDepth = 1
	@property
	def toDict(self):
		import logging
		from tuition.settings import DEFAULT_DATE_INPUT_FORMATS

		output = SortedDict()
		# set the key of the entity in the output dict.
		try:
			output['key'] = str(self.key())
		except NotSavedError as e:
			output['key'] = ''
			logging.info('Error occurred while serializing %s. %s' % (self.__class__.__name__, e.message))
			pass

		try:
			output['name'] = self.name
		except AttributeError as e:
			logging.info(e.message)
			pass
		try:
			output['calendarReminderURL'] = self.calendarReminderURL
		except AttributeError as e:
			logging.info(e.message)
			pass

		for key, prop in self.properties().iteritems():
			value = getattr(self, key)
			if value is None or isinstance(value, BASIC_TYPES):
				output[key] = value
			elif isinstance(value, datetime.date):
				output[key] = value.strftime(DEFAULT_DATE_INPUT_FORMATS)
			elif isinstance(value, db.Model) and self.maxDepth == 1:
				self.maxDepth += 1
				output[key] = value.toDict
			else:
				raise ValueError('Cannot encode ' + repr(prop))
		return output