class ExpensesWrapper(object):
	from models import Expenses

	model = Expenses

	def getForPeriod(self, userKey, start, end):
		return self.model.all().filter(
			'user =', userKey
		).filter(
			'dateOfExpense >=', start
		).filter(
			'dateOfExpense <=', end
		).order(
			'-dateOfExpense'
		).fetch(limit=1000)

class DebtWrapper(object):
	from models import Debt

	model = Debt

	def getForPeriod(self, userKey, start, end):
		return self.model.all().filter(
			'user =', userKey
		).filter(
			'incurredDate >=', start
		).filter(
			'incurredDate <=', end
		).order(
			'-incurredDate'
		).fetch(limit=1000)

	def canDelete(self, debt):
		from tuition.common.customExceptions import CannotDeleteException

		if debt.hasReturned:
			raise CannotDeleteException('Debt Already Returned.')
		return str(debt.amount)

	def delete(self, key):
		debt = self.model.get(key)
		amount = self.canDelete(debt)
		if amount:
			debt.delete()
			return amount
		return False
