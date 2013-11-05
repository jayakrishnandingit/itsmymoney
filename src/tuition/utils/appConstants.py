from tuition.settings import IS_DEV_ENV
import calendar

FB_APP_ID = '596228337059631'
FB_SECRET_KEY = '65b059c58b952c2299bbe86b3b7aecf6'

APP_DOMAIN = 'gcdc2013-itsmymoney.appspot.com'
# Read the below article before we start implementing openID.
# Currently we implement only google login.
# https://developers.google.com/appengine/articles/openid
OPEN_ID_PROVIDERS = {
    'google' : 'https://www.google.com/accounts/o8/id'
    # add more open id providers here. but before that we may need to implement a new login page!
}

LOGOUT_URLS = {
    'google' : 'https://www.google.com/accounts/Logout?continue=http://appengine.google.com/_ah/logout?continue=http://%s%s'
}

GOOGLE_API_WEB_APP_CLIENT_ID = '1078565712000.apps.googleusercontent.com'
GOOGLE_API_WEB_APP_CLIENT_SECRET = 'kNIC0A7YPydFr3FHx8nG5x88'
GOOGLE_API_SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/plus.login']

MONTH_NUM_FULL_NAME_DICT = {i+1:calendar.month_name[i+1] for i in xrange(12)}

if IS_DEV_ENV:
	from localAppConstants import *