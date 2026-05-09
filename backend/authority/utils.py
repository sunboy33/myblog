from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
import smtplib




def send_email(to_addr, subject, msg):
    from_addr = settings.EMAIL_HOST_USER
    auth_code = settings.EMAIL_HOST_PASSWORD
    server = settings.SMTP_SERVER
    port = settings.SMTP_PORT

    obj = MIMEMultipart()
    obj['From'] = f'"YoY" <{from_addr}>'
    obj['To'] = to_addr
    obj['Subject'] = Header(subject, 'utf-8')
    obj.attach(MIMEText(msg, 'html', 'utf-8'))

    try:
        smtpobj = smtplib.SMTP_SSL(server, port)
        smtpobj.login(from_addr, auth_code)
        smtpobj.sendmail(from_addr, to_addr, obj.as_string())
        return True
    except smtplib.SMTPException as e:
        print('发送邮件失败!', e)
        return False
    finally:
        smtpobj.quit()