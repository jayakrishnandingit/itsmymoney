def contextProcessor(request):
	import datetime
	from tuition.settings import SITE_SUPPORT_EMAIL
	from tuition.utils.utils import ExportHandle, ExportClassHandle
	from tuition.utils.manager import AppManager

	return {
		'url' : AppManager.createLogoutURL(),
		'homePage' : '/',
		'supportEmail'       : SITE_SUPPORT_EMAIL,
		'spreadSheetHandle' : ExportHandle.SPREADSHEET,
		'expenseExportHandle' : ExportClassHandle.EXPENSE,
		'debtExportHandle' : ExportClassHandle.DEBT,
		'startOfMonth' : datetime.date.today().replace(day=1)
	}