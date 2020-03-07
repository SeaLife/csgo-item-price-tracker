import smtplib
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail():
    str_from = os.getenv('MAIL_FROM', 'csgo-item-info@example.com')
    str_to = os.getenv('MAIL_TO', 'root@localhost')
    subject = os.getenv('MAIL_SUBJECT', 'Counter-Strike Global Offensive - Item Prices')

    msg_root = MIMEMultipart('related')
    msg_root['Subject'] = subject
    msg_root['From'] = str_from
    msg_root['To'] = str_to

    msgText = MIMEText(
        'The Prices of your Items may have changed! Take a look at the chart! :)<br><br><img src="cid:image1"></img>',
        'html')
    msg_root.attach(msgText)

    fp = open('chart.png', 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()

    msg_image.add_header('Content-ID', '<image1>')
    msg_root.attach(msg_image)

    print(f">> sending mail to {str_to} via {os.getenv('MAIL_SMTP_HOST')}:{os.getenv('MAIL_SMTP_PORT')}.")

    smtp = smtplib.SMTP(os.getenv('MAIL_SMTP_HOST', 'smtp.example.com'))
    smtp.connect(os.getenv('MAIL_SMTP_HOST', 'smtp.example.com'), int(os.getenv('MAIL_SMTP_PORT', '587')))

    if bool(os.getenv('MAIL_SMTP_TLS', '0')):
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

    smtp.login(os.getenv('MAIL_SMTP_USER'), os.getenv('MAIL_SMTP_PASSWORD'))
    smtp.sendmail(str_from, str_to, msg_root.as_string())
    smtp.quit()
