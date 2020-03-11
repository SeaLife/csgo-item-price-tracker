import logging
import smtplib
import os
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

log = logging.getLogger("mail")

SMTP_HOST = os.getenv('MAIL_SMTP_HOST')
SMTP_PORT = int(os.getenv('MAIL_SMTP_PORT', '587'))
SMTP_TLS = bool(os.getenv('MAIL_SMTP_TLS', '0'))

SMTP_USERNAME = os.getenv('MAIL_SMTP_USER')
SMTP_PASSWORD = os.getenv('MAIL_SMTP_PASSWORD')

MAIL_RECEIVER = os.getenv('MAIL_RECEIVER')
MAIL_SENDER = os.getenv('MAIL_SENDER', SMTP_USERNAME)


class Mail:
    root = MIMEMultipart('related')

    def __init__(self, subject: str, receiver: str = MAIL_RECEIVER, sender: str = MAIL_SENDER):
        self.root['Subject'] = subject
        self.root['From'] = sender
        self.root['To'] = receiver

    def add_image(self, path, name):
        img = open(path, 'rb')
        mail_image = MIMEImage(img.read())
        mail_image.add_header('Content-ID', f'<{name}>')
        img.close()
        self.root.attach(mail_image)

    def add_text(self, text, message_type: str = 'html'):
        text = MIMEText(text, message_type)
        self.root.attach(text)

    def send(self):
        smtp = smtplib.SMTP(SMTP_HOST)

        try:
            smtp.connect(SMTP_HOST, SMTP_PORT)

            if SMTP_TLS is True:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()

            log.debug("SMTP authentication as %s", SMTP_USERNAME)
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            log.debug("SMTP sending mail to %s as %s", self.root['To'], self.root['From'])
            smtp.sendmail(self.root["From"], self.root["To"], self.root.as_string())
            log.info("Mail sent to %s", self.root['To'])
            smtp.quit()
        except ConnectionRefusedError:
            log.error(f"Failed to send mail, connection was refused (host={SMTP_HOST},port={SMTP_PORT}).")
