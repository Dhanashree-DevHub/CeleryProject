from celery import shared_task
from .models import Report
from django.core.mail import send_mail
import time
import logging

logger = logging.getLogger(__name__)

@shared_task(name="dummy_and_slow")
def dummy_and_slow():
    time.sleep(2)
    logger.debug("Dummy and slow task has finished")
    
@shared_task(name="mainapp_generate_report")
def generate_report(report_id):
    report = Report.objects.get(id=report_id)
    report.generate()
    
    
@shared_task(name="send_email")
def send_feedback_email(email_address,message):
    time.sleep(20)
    send_mail(
                "Your Feedback",
        f"\t{message}\n\nThank you!",
        "support@example.com",
        [email_address],
        fail_silently=False,
    )