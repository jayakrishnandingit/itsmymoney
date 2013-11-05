import appengine_config
from django.conf import settings
settings._target = None

from google.appengine.ext.webapp import util
from django.core.handlers import wsgi
import django.core.signals
import django.db
import django.dispatch
import logging

def log_exception(*args, **kwds):
    logging.exception('Exception in request:')

# Log errors.
django.dispatch.Signal.connect(
    django.core.signals.got_request_exception, log_exception)

# Unregister the rollback event handler.
django.dispatch.Signal.disconnect(
    django.core.signals.got_request_exception,
    django.db._rollback_on_exception)

# This is how you must run your application in python27 runtime. The below line should be in a global scope.
# @see: https://developers.google.com/appengine/docs/python/tools/libraries27#django
application = wsgi.WSGIHandler()

# This is the old code, python2.5 way.
# def main():
#     application = wsgi.WSGIHandler()
#     util.run_wsgi_app(application)

# if __name__ == '__main__':
#     main()
