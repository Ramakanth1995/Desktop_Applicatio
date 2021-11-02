import email
import smtplib
import threading
from tkinter import messagebox
from common import Values, Config as properties

sender = properties.get_setting(Values.GENERAL_SECTION,Values.SENDER_EMAIL)
sender_password = properties.get_setting(Values.GENERAL_SECTION,Values.SENDER_EMAIL_PASSWORD)


class Mail(threading.Thread):

    def __init__(self,receiver_email_id,user_email,password=None):
        super().__init__()
        self._receiver_email_id = receiver_email_id
        self._username = user_email
        self._password = password
        self._message = None

    def set_create_login_message(self):
        self._message = "Here is your user credential\n username : {} , password : {}"\
            .format(self._username, self._password)

    def set_update_login_message(self):
        self._message = "Your user credentials are updated\n username : {} , password : {}" \
            .format(self._username, self._password)

    def set_delete_login_message(self):
        self._message = "Your account with username : {} is deleted.\nPlease contact administrator" \
                        "for further details." \
            .format(self._username)

    def _send_mail(self):
        try:
            msg = email.message.Message()
            msg['Subject'] = 'Your User Credentials'
            msg['From'] = sender
            msg['To'] = self._receiver_email_id
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload("""<b>{}</b>""".format(self._message, ))

            smtp = smtplib.SMTP(Values.SMTP_SERVER, Values.SMTP_SERVER_PORT)
            smtp.starttls()
            smtp.login(sender, sender_password)
            smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
            smtp.close()
            print("Successfully sent email")

        except smtplib.SMTPException as smtpexec:
            messagebox.showerror("Error","unable to send email\nError : "+str(smtpexec))

    def run(self):
        self._send_mail()