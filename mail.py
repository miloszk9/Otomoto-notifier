import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#The mail addresses and password
sender_address = 'miloszk990@gmail.com'
sender_pass = '...'
receiver_address = 'miloszk1990@gmail.com'
#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = "Test email"

mail_content = """\
<html>
  <body>
    <p><b>Python Mail Test</b><br>
       This is HTML email with attachment.<br>
       Click  <a href="https://interia.com">interia</a> 
    </p>
  </body>
</html>
"""
#mail_content = "# Test email"

#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'html'))
#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login(sender_address, sender_pass) #login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print('Mail Sent')