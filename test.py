import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = 'sales@webapphealing.com'  # Replace with your email address
sender_password = '7,%^{HirXEOI'  # Replace with your email password
receiver_email = 'harshitgadhiya8980@gmail.com'  # Replace with the recipient's email address
subject = 'merge Request'
message = 'Hello this mail is for review the code'

# Create a multipart message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the message to the email
msg.attach(MIMEText(message, 'plain'))

# SMTP connection
try:
    server = smtplib.SMTP('mail.webapphealing.com', 587)  # Replace with the Hostinger SMTP server and port
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print('Email sent successfully!')
except Exception as e:
    print('Error sending email:', str(e))
finally:
    server.quit()





# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Email configuration
# sender_email = 'kakadiyajay@yahoo.com'  # Replace with your Yahoo email address
# sender_password = 'business@63522'  # Replace with your Yahoo email password
# receiver_email = 'jp738317@gmail.com'  # Replace with the recipient's email address
# subject = 'Hello from Python!'
# message = 'This is a test email sent using Python.'

# # Create a multipart message
# msg = MIMEMultipart()
# msg['From'] = sender_email
# msg['To'] = receiver_email
# msg['Subject'] = subject

# # Attach the message to the email
# msg.attach(MIMEText(message, 'plain'))

# # SMTP connection
# try:
#     server = smtplib.SMTP('smtp.mail.yahoo.com', 587)  # Replace with the Yahoo SMTP server and port
#     server.starttls()
#     server.login(sender_email, sender_password)
#     server.sendmail(sender_email, receiver_email, msg.as_string())
#     print('Email sent successfully!')
# except Exception as e:
#     print('Error sending email:', str(e))
# finally:
#     server.quit()



# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Email configuration
# sender_email = 'jaykakadiya2014@outlook.com'  # Replace with your Outlook email address
# sender_password = 'jaykakadiyA2*'  # Replace with your Outlook email password
# receiver_email = 'jp738317@gmail.com'  # Replace with the recipient's email address
# subject = 'Hello from Python!'
# message = 'This is a test email sent using Python.'

# # Create a multipart message
# msg = MIMEMultipart()
# msg['From'] = sender_email
# msg['To'] = receiver_email
# msg['Subject'] = subject

# # Attach the message to the email
# msg.attach(MIMEText(message, 'plain'))

# # SMTP connection
# try:
#     server = smtplib.SMTP('smtp.office365.com', 587)  # Replace with the Outlook SMTP server and port
#     server.starttls()
#     server.login(sender_email, sender_password)
#     server.sendmail(sender_email, receiver_email, msg.as_string())
#     print('Email sent successfully!')
# except Exception as e:
#     print('Error sending email:', str(e))
# finally:
#     server.quit()