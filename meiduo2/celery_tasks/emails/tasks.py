from django.core.mail import send_mail
from celery_tasks.main import app

@app.task
def send_emails(user_id,email):
    subject = '美多测试'
    message = ''
    from_email = '管理员<15893775982@163.com>'
    recipient_list = ['15893775982@163.com']
    html_message = "<a href='http://www.meiduo.site:8000/emailsactive/?token=1'>这是一个标签</a>"

    send_mail(subject=subject,
              message=message,
              from_email=from_email,
              recipient_list=recipient_list,
              html_message=html_message)
