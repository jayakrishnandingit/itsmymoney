from oauth2client.appengine import OAuth2DecoratorForDjango, OAuth2DecoratorFromClientSecrets
from appConstants import GOOGLE_API_WEB_APP_CLIENT_ID, GOOGLE_API_WEB_APP_CLIENT_SECRET, GOOGLE_API_SCOPES

decorator = OAuth2DecoratorForDjango(
    client_id=GOOGLE_API_WEB_APP_CLIENT_ID,
    client_secret=GOOGLE_API_WEB_APP_CLIENT_SECRET,
    scope=GOOGLE_API_SCOPES,
    callback_path='oauth2callback'
)