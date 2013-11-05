class HandleRequests(object):
    def process_request(self, request):
        import logging
        from django import http
        from django.shortcuts import render_to_response
        from django.template import RequestContext
        from tuition.settings import SITE_DOWN_FOR_MAINTENANCE, SITE_DOWN_DESCRIPTION, SITE_SUPPORT_EMAIL
        from tuition.utils.manager import AppManager

        AppManager.setDomain(request.get_host())
        if AppManager.isCurrentUserAppAdmin():
            return None

        url = AppManager.isUserLoggedIn(request.path, request.path)
        if url:
            logging.info('User has not logged in.')
            logging.info('Going to redirect user to %s.' % url)
            return http.HttpResponseRedirect(url)

        user = AppManager.getCurrentLoggedInUser()
        if user:
            if SITE_DOWN_FOR_MAINTENANCE:
                return render_to_response(
                    'siteDown.html', 
                    {'description' : SITE_DOWN_DESCRIPTION}, 
                    context_instance=RequestContext(request)
                )
            # implement any OAuth in future.
            if not AppManager.getUserByEmail(user.email()) and request.path not in SAFE_TO_REDIRECT_URI:
                logging.info('User has not registered yet.')
                logging.info('Going to redirect user to /register')
                return http.HttpResponseRedirect('/register?firstLogin=1')
            return None
        return None

SAFE_TO_REDIRECT_URI = [
    '/register',
    '/ajaxCall/saveUser',
    '/oauth2callback'
]