from exceptions import Exception

class CannotDeleteException(Exception):
	def __init__(self, message, *args, **kwargs):
		super(CannotDeleteException, self).__init__(*args, **kwargs)
		self.message = message
