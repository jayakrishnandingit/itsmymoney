'''
Created on Feb 6, 2013

@author: jayakrishnan
'''
import datetime
from google.appengine.api import users
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import http

def addAnExpense(request):
    from tuition.settings import SITE_SUPPORT_EMAIL
    from forms import ExpenseForm
    from tuition.utils.manager import AppManager

    form = ExpenseForm(initial={'dateOfExpense' : datetime.date.today().strftime('%d/%m/%Y')})
    template_values = {
                       'form'               : form,
                       'loggedInEmployee'   : AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
                       }
    return render_to_response('newExpense.html', template_values, context_instance=RequestContext(request))

def viewUserExpenses(request, userKey=None):
    from tuition.settings import SITE_SUPPORT_EMAIL
    from tuition.utils.manager import AppManager
    from models import Expenses
    from forms import ExpenseForm, ExpenseYearFilter
    from tuition.utils.appConstants import MONTH_NUM_FULL_NAME_DICT
    from tuition.utils.utils import ExportHandle, ExportClassHandle

    loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
    form = ExpenseForm(initial={'dateOfExpense' : datetime.date.today().strftime('%d/%m/%Y')})
    template_values = {
                       'loggedInEmployee'   : loggedInEmployee,
                       'yearFilterForm'     : ExpenseYearFilter(),
                       'monthNameDict'      : MONTH_NUM_FULL_NAME_DICT,
                       'exportHandle'       : ExportHandle.asDict(),
                       'classHandle'        : ExportClassHandle.asDict(),
                       'form'               : form
                       }
    return render_to_response('viewExpenses.html', template_values, context_instance=RequestContext(request))

def export(request):
  import datetime
  from tuition.settings import SITE_SUPPORT_EMAIL
  from tuition.utils.manager import AppManager
  from tuition.utils.utils import ExportSelector, EXPORT_HANDLE_LABELS, getMonthEnd

  serializedObjectList = []
  linkToFile = None
  fileName = None
  isSaved = False
  noData = True
  invalidHandle = True
  response = {}

  classHandle = request.GET.get('classHandle', None)
  exportHandle = request.GET.get('handle', None)
  exportDate = datetime.datetime.strptime(request.GET.get('date', datetime.date.today().strftime('%d_%m_%Y')), '%d_%m_%Y')
  firstOfMonth = datetime.date(exportDate.year, exportDate.month, 1)
  endOfMonth = datetime.date(exportDate.year, exportDate.month, getMonthEnd(exportDate.month, exportDate.year))
  loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())

  classWrapper = ExportSelector.getClass(classHandle)
  dataList = classWrapper().getForPeriod(loggedInEmployee.key(), firstOfMonth, endOfMonth)
  if dataList:
    noData = False
    for data in dataList:
      serializedObjectList.append(data.toDict)
    exporterClass = ExportSelector.getHandle(exportHandle)
    if exporterClass:
      invalidHandle = False
      exporterInstance = exporterClass(
          serializedObjects=serializedObjectList, 
          request=request, 
          remove=['key', 'user', 'calendarReminderURL', 'createdOn', 'updatedOn'],
          date=exportDate,
          namePrefix=classHandle
      )
      response = exporterInstance.upload()
  if isinstance(response, dict):
    isSaved = response.get('isSaved')
    linkToFile = response.get('fileResponse', {}).get('alternateLink')
    fileName = response.get('fileResponse', {}).get('title')
    template_values = {
      'isSaved'            : isSaved, 
      'linkToFile'         : linkToFile,
      'fileName'           : fileName,
      'handle'             : EXPORT_HANDLE_LABELS.get(exportHandle, exportHandle),
      'classHandle'        : classHandle,
      'invalidHandle'      : invalidHandle,
      'noData'             : noData,
      'loggedInEmployee'   : loggedInEmployee
    }
    return render_to_response('exportFinish.html', template_values, context_instance=RequestContext(request))
  else:
    return response

def viewUserDebts(request, userKey=None):
    from tuition.settings import SITE_SUPPORT_EMAIL
    from tuition.utils.manager import AppManager
    from models import Debt
    from forms import DebtForm, ExpenseYearFilter, DebtReturnForm
    from tuition.utils.appConstants import MONTH_NUM_FULL_NAME_DICT
    from tuition.utils.utils import ExportHandle, ExportClassHandle

    # keyToSetReminder = request.GET.get('key', None)
    # if keyToSetReminder:
    #   debt = Debt.get(keyToSetReminder)
    #   serializedObjectList = [debt.toDict]
    #   GoogleCalendarService()
    loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
    form = DebtForm(initial={'incurredDate' : datetime.date.today().strftime('%d/%m/%Y')})
    markAsReturnForm = DebtReturnForm()
    template_values = {
                       'loggedInEmployee'   : loggedInEmployee,
                       'yearFilterForm'     : ExpenseYearFilter(),
                       'monthNameDict'      : MONTH_NUM_FULL_NAME_DICT,
                       'exportHandle'       : ExportHandle.asDict(),
                       'classHandle'        : ExportClassHandle.asDict(),
                       'form'               : form,
                       'markAsReturnForm'   : markAsReturnForm
                       }
    return render_to_response('viewDebts.html', template_values, context_instance=RequestContext(request))

def addADebt(request):
    from tuition.settings import SITE_SUPPORT_EMAIL
    from forms import DebtForm
    from tuition.utils.manager import AppManager

    form = DebtForm(initial={'incurredDate' : datetime.date.today().strftime('%d/%m/%Y')})
    template_values = {
                       'form'               : form,
                       'loggedInEmployee'   : AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
                       }
    return render_to_response('newDebt.html', template_values, context_instance=RequestContext(request))
