from django.shortcuts import render_to_response
from django.template import RequestContext
from django import http

def register(request):
	from tuition.settings import SITE_SUPPORT_EMAIL
	from forms import UserRegistrationForm	
	from tuition.utils.manager import AppManager
	from tuition.utils.utils import URLCreator
	from tuition.urlPatterns import UrlPattern
	from tuition.utils.utils import GooglePlusService

	queryString = int(request.GET.get('firstLogin', 0))
	loggedInEmployee = AppManager.getCurrentLoggedInUser()
	if not AppManager.isCurrentUserAppAdmin():
		if not queryString or AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email()):
			raise Exception('Unauthorized Access')
	else:
		loggedInEmployee = AppManager.getUserByEmail(AppManager.getCurrentLoggedInUser().email())
	template_values = {
		'form' : UserRegistrationForm(),
		'loggedInEmployee' : loggedInEmployee,
		'queryString' : queryString
	}
	return render_to_response('userRegistration.html', template_values, context_instance=RequestContext(request))

def profile(request):
	from tuition.settings import SITE_SUPPORT_EMAIL
	from tuition.utils.utils import GooglePlusService
	from tuition.utils.manager import AppManager
	from forms import UserRegistrationForm

	user = AppManager.getCurrentLoggedInUser()
	loggedInEmployee = AppManager.getUserByEmail(user.email())
	loggedInEmployee.id = user.user_id()
	response = GooglePlusService(request=request, loggedInEmployee=loggedInEmployee).getUserInfo(setImageSize=250)
	if isinstance(response, dict):
		locationFromPlus = response.get('userInfo', {}).get('currentLocation', '')
		if not locationFromPlus:
			placesLived = response.get('userInfo', {}).get('placesLived', [])
			if placesLived and placesLived[0].get('primary'):
				locationFromPlus = placesLived[0].get('value')
		template_values = {
			'form' : UserRegistrationForm(initial={
				'firstName' : loggedInEmployee.firstName,
				'lastName'  : loggedInEmployee.lastName,
				'alternateEmail' : loggedInEmployee.alternateEmail,
				'dob' : loggedInEmployee.dob.strftime('%d/%m/%Y'),
				'about' : loggedInEmployee.about or ''
			}),
			'loggedInEmployee' : loggedInEmployee,
			'publicProfile' : response.get('userInfo', {}).get('url', '#'),
			'imageUrl' : response.get('userInfo', {}).get('image', {}).get('url', '/images/emptyProfile.gif'),
			'locationFromPlus' : locationFromPlus,
			'about' : response.get('userInfo', {}).get('aboutMe', '')
		}
		return render_to_response('userProfile.html', template_values, context_instance=RequestContext(request))
	return response