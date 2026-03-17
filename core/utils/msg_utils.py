import requests
from django.core.mail import EmailMessage

# HireSure Includes
import hq.settings as site_settings
import core.settings as core_settings


def send_message_91(number, message):
    headers = {'authkey':core_settings.MSG91_KEY,
               'Content-Type':'application/json'}
    data = {"sender": "HRSURE",
        "route": "4",
        "country": "91",
        "sms": [{
                "message": message,
                "to": [number,]
            }]
        }
    r= requests.post(core_settings.MSG91_URL, json=data, headers=headers)
    if (r.status_code == 200):
        return True
    else:
        return False

def mail_to_admin(message):
    msg = EmailMessage(subject='Imp: Message for admin ['+site_settings.BASE_URL+']',
                       body=message,
                       from_email=site_settings.DEFAULT_FROM_EMAIL,
                       to=site_settings.HS_OWNER_EMAILS,)
    msg.send(fail_silently=False)

