from django import http
from google.appengine.ext import db

class JSONParser(object):

	def get(self, data):
		from django.utils import simplejson

		return simplejson.loads(data)

	def respond(self, **data):
		from django.utils import simplejson

		return simplejson.dumps(data)

def mainHandler(request, functionName):
	from django.utils import simplejson

	if not functionName:
		raise Exception()
	args = simplejson.loads(request.POST.get('arg', '[]'))
	ajaxMainClass = AjaxMethods()
	ajaxMainClass.httpRequest = request
	funtionToCall = getattr(ajaxMainClass, functionName, None)
	if not funtionToCall:
		return http.Http404

	responseValues = funtionToCall(*args)
	response = http.HttpResponse()
	response.status_code = 200
	response.write(responseValues)
	response['Content-Type'] = 'application/json'
	return response

class AjaxMethods(JSONParser):
	httpRequest = None

	def saveUser(self, serializedFormValues):
		from google.appengine.ext import deferred
		from tuition.user.models import User
		from tuition.utils.manager import AppManager
		from tuition.utils.mailer import SendNotification
		from tuition.user.forms import UserRegistrationForm

		isEdit = False
		loggedInEmployee = AppManager.getCurrentLoggedInUser()
		email = loggedInEmployee.email()
		form = UserRegistrationForm(data=serializedFormValues)
		if serializedFormValues.get('keyHidden'):
			isEdit = True
			loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
			form.loggedInEmployeeKey = str(loggedInEmployee.key())
			form.keyHidden = serializedFormValues.get('keyHidden')
			email = loggedInEmployee.email
		if form.is_valid():
			dictToSave = {
				'firstName' : form.cleaned_data['firstName'],
				'lastName' : form.cleaned_data['lastName'],
				'email' : email,
				'alternateEmail' : form.cleaned_data['alternateEmail'],
				'dob' : form.cleaned_data['dob'],
				'about' : form.cleaned_data['about']
			}
			if not isEdit:
				savedUser = User(**dictToSave)
				savedUserKey = db.put(savedUser)
				deferred.defer(SendNotification().sendRegistrationSuccessMail, str(savedUserKey))
			else:
				savedUser = User.get(serializedFormValues.get('keyHidden'))
				for key, value in dictToSave.iteritems():
					setattr(savedUser, key, value)
				savedUserKey = db.put(savedUser)
			return self.respond(
				isSaved=True, 
				isEdit=isEdit,
				savedUserKey=str(savedUserKey),
				savedValues=savedUser.toDict
			)
		else:
			return self.respond(
				isSaved=False, 
				errors=form.errors
			)

	def getTodaysExpense(self):
		import datetime
		from tuition.tools.models import Expenses
		from tuition.utils.manager import AppManager

		serializedObjects = []
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		today = datetime.date.today()
		todaysExpense = Expenses.all().filter('user =', loggedInEmployee.key()).filter('dateOfExpense =', today).order('-dateOfExpense')
		todaysExpense = todaysExpense.fetch(limit=1000)
		for expense in todaysExpense:
			serializedObjects.append(expense.toDict)
		return self.respond(expenses=serializedObjects)

	def getExpenseThisWeek(self):
		import datetime
		from tuition.tools.models import Expenses
		from tuition.utils.manager import AppManager
		from tuition.utils.utils import weekStartEnd

		serializedObjects = []
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		startOfWeek = weekStartEnd().get('start')
		thisWeeksExpense = Expenses.all().filter('user =', loggedInEmployee.key()).filter('dateOfExpense >=', startOfWeek).order('-dateOfExpense')
		thisWeeksExpense = thisWeeksExpense.fetch(limit=1000)
		for expense in thisWeeksExpense:
			serializedObjects.append(expense.toDict)
		return self.respond(expenses=serializedObjects)

	def getExpenseThisMonth(self, values):
		import datetime
		from tuition.tools.models import Expenses
		from tuition.utils.manager import AppManager
		from tuition.utils.utils import getMonthEnd

		serializedObjects = []
		year = int(values.get('year', 2013))
		month = int(values.get('month', datetime.date.today().month))
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		firstOfMonth = datetime.date(year, month, 1)
		endOfMonth = datetime.date(year, month, getMonthEnd(month, year))
		thisMonthExpense = Expenses.all().filter('user =', loggedInEmployee.key()).filter('dateOfExpense >=', firstOfMonth).filter('dateOfExpense <=', endOfMonth).order('-dateOfExpense')
		thisMonthExpense = thisMonthExpense.fetch(limit=1000)
		for expense in thisMonthExpense:
			serializedObjects.append(expense.toDict)
		return self.respond(expenses=serializedObjects)

	def getExpenseOfYear(self, value):
		import datetime
		from tuition.tools.models import Expenses
		from tuition.utils.manager import AppManager
		from tuition.utils.appConstants import MONTH_NUM_FULL_NAME_DICT

		serializedList = []
		year = int(value.get('year', 2013))
		dateToCheck = datetime.date(year, 1, 1)
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		expenseOfTheYear = Expenses.all().filter('user =', loggedInEmployee.key()).filter('dateOfExpense >=', dateToCheck).fetch(1000)
		for expense in expenseOfTheYear:
			serializedList.append(expense.toDict)
		return self.respond(expenses=serializedList)

	def saveAnExpense(self, serializedFormValues):
		from tuition.utils.manager import AppManager
		from tuition.tools.forms import ExpenseForm
		from tuition.tools.models import Expenses

		form = ExpenseForm(data = serializedFormValues)
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		if form.is_valid():
			dictToSave = {
			    'user' 				: loggedInEmployee.key(),
			    'type'				: form.cleaned_data['type'],
			    'amount'			: form.cleaned_data['amount'],
			    'dateOfExpense'		: form.cleaned_data['dateOfExpense'],
			    'comments'			: form.cleaned_data['comments']
			}
			newExpense = Expenses(**dictToSave)
			return self.respond(isSaved=True, savedExpenseKey=str(db.put(newExpense)))
		else:
			return self.respond(isSaved=False, errors=form.errors)

	def deleteAnExpense(self, expenseKey):
		from google.appengine.ext import db
		from tuition.tools.models import Expenses

		expenseToDelete = Expenses.get(expenseKey)
		amount = expenseToDelete.amount
		db.delete(expenseToDelete.key())
		isSaved = True
		return self.respond(isSaved=isSaved, key=expenseKey, amount=amount)

	def saveDebt(self, serializedFormValues):
		from tuition.utils.manager import AppManager
		from tuition.tools.forms import DebtForm
		from tuition.tools.models import Debt, Expenses

		modelsToPut = []
		savedExpenseKey = None
		savedDebtKey = None
		form = DebtForm(data = serializedFormValues)
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		if form.is_valid():
			dictToSave = {
			    'user' 				: loggedInEmployee.key(),
			    'type'				: form.cleaned_data['type'],
			    'amount'			: form.cleaned_data['amount'],
			    'incurredDate'		: form.cleaned_data['incurredDate'],
			    'returnDate'		: form.cleaned_data['returnDate'],
			    'expenseOfMonth'	: form.cleaned_data['expenseOfMonth'],
			    'hasReturned'		: form.cleaned_data['hasReturned'],
			    'comments'			: form.cleaned_data['comments']
			}
			newDebt = Debt(**dictToSave)
			modelsToPut.append(newDebt)

			if form.cleaned_data['hasReturned']:
				dictToSave = {
			    'user' 				: loggedInEmployee.key(),
			    'type'				: 'Debt Return',
			    'amount'			: newDebt.amount,
			    'dateOfExpense'		: form.cleaned_data['expenseOfMonth'],
			    'comments'			: ''
				}
				newExpense = Expenses(**dictToSave)
				modelsToPut.append(newExpense)

			if len(modelsToPut) > 1:
				savedDebtKey, savedExpenseKey = db.put(modelsToPut)
			elif len(modelsToPut) == 1:
				savedDebtKey = db.put(modelsToPut)
			return self.respond(
				isSaved=True, 
				savedDebtKey=str(savedDebtKey),
				savedExpenseKey=str(savedExpenseKey),
				savedDebt=newDebt.toDict
			)
		else:
			return self.respond(isSaved=False, errors=form.errors)

	def deleteDebt(self, keyToDelete):
		import logging
		from google.appengine.ext import db
		from tuition.tools.modelWrapper import DebtWrapper
		from tuition.common.customExceptions import CannotDeleteException

		try:
			amount = DebtWrapper().delete(db.Key(keyToDelete))
			isSaved = True
		except CannotDeleteException as e:
			logging.error(e.message)
			isSaved = False
			amount = 0

		return self.respond(isSaved=isSaved, key=keyToDelete, amount=amount)

	def getTodaysDebt(self):
		import datetime
		from tuition.tools.models import Debt
		from tuition.utils.manager import AppManager

		serializedObjects = []
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		today = datetime.date.today()
		todaysDebt = Debt.all().filter('user =', loggedInEmployee.key()).filter('incurredDate =', today).order('-incurredDate')
		todaysDebt = todaysDebt.fetch(limit=1000)
		for debt in todaysDebt:
			serializedObjects.append(debt.toDict)
		return self.respond(debts=serializedObjects)

	def getDebtThisWeek(self):
		import datetime
		from tuition.tools.models import Debt
		from tuition.utils.manager import AppManager
		from tuition.utils.utils import weekStartEnd

		serializedObjects = []
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		startOfWeek = weekStartEnd().get('start')
		thisWeeksDebt = Debt.all().filter('user =', loggedInEmployee.key()).filter('incurredDate >=', startOfWeek).order('-incurredDate')
		thisWeeksDebt = thisWeeksDebt.fetch(limit=1000)
		for debt in thisWeeksDebt:
			serializedObjects.append(debt.toDict)
		return self.respond(debts=serializedObjects)

	def getDebtThisMonth(self, values):
		import datetime
		from tuition.tools.models import Debt
		from tuition.utils.manager import AppManager
		from tuition.utils.utils import getMonthEnd

		serializedObjects = []
		year = int(values.get('year', 2013))
		month = int(values.get('month', datetime.date.today().month))
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		firstOfMonth = datetime.date(year, month, 1)
		endOfMonth = datetime.date(year, month, getMonthEnd(month, year))
		thisMonthDebts = Debt.all().filter('user =', loggedInEmployee.key()).filter('incurredDate >=', firstOfMonth).filter('incurredDate <=', endOfMonth).order('-incurredDate')
		thisMonthDebts = thisMonthDebts.fetch(limit=1000)
		for debt in thisMonthDebts:
			serializedObjects.append(debt.toDict)
		return self.respond(debts=serializedObjects)

	def getDebtOfYear(self, value):
		import datetime
		from tuition.tools.modelWrapper import DebtWrapper
		from tuition.utils.manager import AppManager
		from tuition.utils.appConstants import MONTH_NUM_FULL_NAME_DICT

		serializedList = []
		year = int(value.get('year', 2013))
		firstOfYear = datetime.date(year, 1, 1)
		endOfYear = datetime.date(year, 12, 31)
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		debtOfTheYear = DebtWrapper().getForPeriod(loggedInEmployee.key(), firstOfYear, endOfYear)
		for debt in debtOfTheYear:
			serializedList.append(debt.toDict)
		return self.respond(debts=serializedList)

	def markDebtReturn(self, serializedFormValues):
		from tuition.tools.models import Expenses, Debt
		from tuition.tools.forms import DebtReturnForm
		from tuition.utils.manager import AppManager

		modelsToPut = []
		form = DebtReturnForm(data = serializedFormValues)
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
		debt = Debt.get(serializedFormValues['key'])
		form.debtIncurredDate = debt.incurredDate
		if form.is_valid() and not debt.hasReturned:
			dictToSave = {
			    'expenseOfMonth'	: form.cleaned_data['markAsExpense'],
			    'hasReturned'		: True
			}
			for key, value in dictToSave.iteritems():
				setattr(debt, key, value)
			modelsToPut.append(debt)
			# we need to mark it as an expense of the given date.
			dictToSave = {
			    'user' 				: loggedInEmployee.key(),
			    'type'				: 'Debt Return',
			    'amount'			: debt.amount,
			    'dateOfExpense'		: form.cleaned_data['markAsExpense'],
			    'comments'			: form.cleaned_data['returnComments']
			}
			expense = Expenses(**dictToSave)
			modelsToPut.append(expense)
			savedDebtKey, savedExpenseKey = db.put(modelsToPut)
			return self.respond(
				isSaved=True, 
				savedDebtKey=str(savedDebtKey),
				savedExpenseKey=str(savedExpenseKey), 
				savedDebt=debt.toDict
			)
		else:
			return self.respond(
				isSaved=False, 
				errors=form.errors, 
				debtAlreadyReturned=debt.hasReturned
			)
