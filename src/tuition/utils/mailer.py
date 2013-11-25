from google.appengine.api import mail
from tuition.settings import SITE_SUPPORT_EMAIL
from appConstants import MAIL_SENDER_NAME, MAIL_SUBJECT_PREFIX

class SendNotification(object):
	def __init__(self, senderName=MAIL_SENDER_NAME, senderEmail=SITE_SUPPORT_EMAIL, **kwargs):
		self.senderName = senderName
		self.senderEmail = senderEmail
		self.senderAddress = '%s<%s>' % (self.senderName, self.senderEmail)
		self.subject = MAIL_SUBJECT_PREFIX

	def sendRegistrationSuccessMail(self, userKey):
		from tuition.user.models import User
		from tuition.utils.manager import AppManager

		user = User.get(userKey)
		to = '%s<%s>' %(user.name, user.email)
		self.subject += 'Successful Registration'
		self.body = '''
			<?xml version="1.0" encoding="UTF-8" ?>
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml">
			<body>
				<div>
					<img src="/images/logo.png" />
				</div>
				<div>
					You have successfully registered with us. <a href="http://%s/user/profile">Visit your profile</a>
				</div>
			</body>
			</html>
		''' % AppManager.getDomain()
		return mail.send_mail(to, self.senderAddress, self.subject, self.body, html=True)
