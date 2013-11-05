def updateExpenses(request):
	from tuition.tools.models import Expenses
	from tuition.utils.manager import AppManager
	from google.appengine.ext import db
	from django import http

	if not AppManager.isCurrentUserAppAdmin():
		raise Exception('Unauthorized Access')

	isOver = False
	pageNo = int(request.GET.get('pageNo', 0))
	expenses = Expenses.all().fetch(limit=60, offset=pageNo*60)
	if expenses:
		for expense in expenses:
			delattr(expense, 'name')
			delattr(expense, 'email')
		db.put(expenses)
		pageNo += 1
	else:
		isOver = True

	content = """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml">
				<head><title>Update Expenses</title></head>
				<body style="font-size: 18px;">
					<div style="text-align:center font-weight:bold">
						Number of records processed in this run : %d
						<form action="/updateExpenses" method="GET">
							<input type="hidden" name="pageNo" value="%d" />
							<input type=submit value="Next"/>
						</form>
					</div>
				</body>
			</html>""" % (len(expenses), pageNo)
	if isOver:
		content = """
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
				<html xmlns="http://www.w3.org/1999/xhtml">
				<head><title>Update Expenses</title></head>
				<body style="font-size: 18px;">
					<div style="text-align:center font-weight:bold">
						Updation Complete
					</div>
				</body>
				</html>
		"""
	response = http.HttpResponse()
	response.write(content)
	return response