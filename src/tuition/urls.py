from django.conf.urls.defaults import patterns, include, handler500, handler404
from tuition.urlPatterns import UrlPattern
from tuition.utils.appConfig import decorator

handler404 = 'tuition.home.views.custom404'
handler500 = 'tuition.home.views.custom500'
urlpatterns = patterns(
                       '',
                       (UrlPattern.HOME, 'tuition.home.views.home'),
                       (UrlPattern.REGISTER_USER, 'tuition.user.views.register'),
                       (UrlPattern.USER_PROFILE, 'tuition.user.views.profile'),
                       (UrlPattern.VIEW_ROLES, 'tuition.role.views.viewRoles'),
                       (UrlPattern.ADD_ROLE, 'tuition.role.views.addRole'),
                       (UrlPattern.VIEW_EXPENSES, 'tuition.tools.views.viewUserExpenses'),
                       (UrlPattern.ADD_EXPENSE, 'tuition.tools.views.addAnExpense'),
                       (UrlPattern.VIEW_DEBTS, 'tuition.tools.views.viewUserDebts'),
                       (UrlPattern.ADD_DEBT, 'tuition.tools.views.addADebt'),
                       (UrlPattern.EXPORT_EXPENSE, 'tuition.tools.views.export'),
                       (UrlPattern.AJAX_CALL, 'tuition.json.ajaxHandler.mainHandler'),
                       (UrlPattern.GOOGLE_API_CALLBACK, decorator.callback_handler),

                       #################### Update script urls starts here. ########################
                       # (r'^updateExpenses$', 'tuition.utils.updateScripts.updateExpenses'),
                       )
