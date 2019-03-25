# views.py

from django.shortcuts import render

def home(req):
    return render(req, 'welcome.html')

#def email(req):
#    '''testing sendgrid'''
#    import os
#    import sendgrid
#    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
#    data = {
#        "personalizations": [{"to": [{"email": "strunstrun@gmail.com"}], "subject": "Sending emails with SendGrid..."}],
#        "from": {"email": "strunstrun@gmail.com"},
#        "content": [{"type": "text/plain", "value": "...is a new possibility."}]
#    }
#    response = sg.client.mail.send.post(request_body=data)
#    print(response.status_code)
#    print(response.body)
#    print(response.headers)
#    return render(req, 'welcome.html')