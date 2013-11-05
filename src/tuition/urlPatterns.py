'''
Created on Dec 3, 2012

@author: jayakrishnan
'''
from tuition.utils.appConfig import decorator

class UrlPattern(object):
    HOME = r'^$'
    AJAX_CALL = r'^ajaxCall/([a-zA-Z]+)$'
    VIEW_ROLES = r'^viewRoles$'
    ADD_ROLE = r'^addRole$'
    VIEW_EXPENSES = r'^viewExpenses$'
    ADD_EXPENSE = r'^addAnExpense$'
    VIEW_DEBTS = r'^viewDebts$'
    ADD_DEBT = r'^addADebt$'
    REGISTER_USER = r'^register$'
    USER_PROFILE = r'^user/profile$'
    EXPORT_EXPENSE = r'^export$'
    GOOGLE_API_CALLBACK = r'^%s$' % decorator.callback_path
