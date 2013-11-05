'''
Created on Nov 9, 2012

@author: jayakrishnan
'''
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    from tuition.settings import SITE_SUPPORT_EMAIL
    from tuition.utils.manager import AppManager, UserFilter

    UserFilter().checkUserRole(request.path)

    template_values = {
                       'loggedInEmployee'   : AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email()),
                       }
    return render_to_response('home.html', template_values, context_instance=RequestContext(request))

def custom404(request):
    from tuition.settings import SITE_SUPPORT_EMAIL

    template_values = {}
    return render_to_response('404.html', template_values, context_instance=RequestContext(request))

def custom500(request):
    from tuition.settings import SITE_SUPPORT_EMAIL

    template_values = {}
    return render_to_response('500.html', template_values, context_instance=RequestContext(request))