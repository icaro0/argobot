## mail sender
import smtplib
from email.message import EmailMessage
class Mail:
    def __init__(self, username, password, server='smtp.gmail.com:587') -> None:
        self.username = username
        self.password = password
        self.server = server
    def enviarmail(self, from_addr, to, subject, message):
        server = smtplib.SMTP(self.server)
        server.starttls()
        server.login(self.username, self.password)
        ## antes de enviar el mail activar aplicaciones menos seguras https://www.google.com/settings/security/lesssecureapps
        em = EmailMessage()
        em.set_content(message)
        em['From'] = from_addr
        em['To'] = to
        em['Subject'] = subject
        server.send_message(em)

        server.quit()