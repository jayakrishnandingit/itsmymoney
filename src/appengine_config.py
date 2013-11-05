import os
# inorder to specify the framework we use is django we write it in app.yaml using libraries directive.
os.environ['DJANGO_SETTINGS_MODULE'] = 'tuition.settings'


# The below package is removed as per the new SDK releases.
# from google.appengine.dist import use_library

# use_library('django', '1.2')
