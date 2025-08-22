from time import sleep
from django.core.mail import send_mail
from django import forms
from mainapp.tasks import send_feedback_email    

class FeedbackForm(forms.Form):
    email=forms.EmailField(label="Email Address")
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={"rows": 5}))
    
    def send_email(self):
        send_feedback_email.delay(self.cleaned_data['email'],self.cleaned_data['message'])        