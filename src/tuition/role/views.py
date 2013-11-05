'''
Created on Dec 3, 2012

@author: jayakrishnan
'''
from django.shortcuts import render_to_response

PERMISSIONS = [
               'BASIC_VIEW',
               'ADD_ROLE',
               'VIEW_ROLES',
               'ADD_STUDENT',
               'EDIT_STUDENT',
               'VIEW_STUDENT',
               'ADD_TEACHER',
               'EDIT_TEACHER',
               'VIEW_TEACHER',
               'ADD_SUBJECT',
               'ADD_GRADE',
               'ADD_EXAM',
               'VIEW_EXAMS'
               ]

PERMISSIONS.sort()

def viewRoles(request):
    from tuition.settings import SITE_SUPPORT_EMAIL
    from tuition.role.models import Role
    from tuition.utils.manager import UserFilter, AppManager

    UserFilter().checkUserRole(request.path)
    roles = Role.all().fetch(limit = 1000)
    template_values = {
                       'loggedInEmployee'   : AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email()),
                       'url'                : AppManager.createLogoutURL(),
                       'homePage'           : '/',
                       'supportEmail'       : SITE_SUPPORT_EMAIL,
                       'roles'              : roles,
                       'permissions'        : PERMISSIONS
                       }
    return render_to_response('viewRoles.html', template_values)

def addRole(request):
    from tuition.settings import SITE_SUPPORT_EMAIL
    from tuition.role.forms import RoleAddForm
    from tuition.utils.manager import UserFilter, AppManager

    UserFilter().checkUserRole(request.path)
    template_values = {
                       'loggedInEmployee'   : AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email()),
                       'url'                : AppManager.createLogoutURL(),
                       'homePage'           : '/',
                       'supportEmail'       : SITE_SUPPORT_EMAIL,
                       'permissions'        : PERMISSIONS,
                       'form'               : RoleAddForm()
                       }
    return render_to_response('addRole.html', template_values)