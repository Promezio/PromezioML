import os
import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.encoders import encode_base64
from getpass import getpass

# Mail server parameters
MAIL_SERVER = "your.mail.server" # CHANGE THIS
MAIL_PORT = 465 # CHANGE THIS
FROM_ADDRESS = "from@test.it" # Change
TO_ADDRESS = "to@test.it" # Change
MAIL_USER = "usename" # Change
MAIL_PASSWORD = "password" # Change


class Email(object):
    ''' A class for send a mail (with attachment) through an 
        SSL SMTP server. The test code work on Raspberry PI with PiCamera.
    '''

    def __init__(self, from_address, to_address, subject, message, image=None):
        # Email data
        self.from_address = from_address
        self.to_address = to_address
        
        # Create the email object
        self.email = MIMEMultipart()

        self.email['From'] = from_address
        self.email['To'] = to_address
        self.email['Subject'] = subject

        text = MIMEText(message, 'plain')
        self.email.attach(text)

        # Manage attachments
        if image != None:
            attachment = MIMEBase('image','jpg')
            attachment.set_payload(image)
            encode_base64(attachment)
            attachment.add_header('Content-Disposition', 
                                   'attachment', 
                                   "image.jpg")
            
            self.email.attach(attachment)

        # Put all email contents in a string
        self.message = self.email.as_string()

    def send(self, username, password):
        # Server data
        server = MAIL_SERVER
        port = MAIL_SERVER_PORT
        
        # Connection
        context = ssl.create_default_context()
        connection = smtplib.SMTP_SSL(server, port, context=context)
        connection.login(username, password)

        # Send the message
        connection.sendmail(self.from_address, 
                            self.to_address, 
                            self.message)
        
        # Close
        connection.close()
        
        
        
 #######################################################       
 # TEST CODE
 # FOR Raspberry PI with PiCamera
 if __name__ == "__main__":
  # Retrieve a frame
  with picamera.PiCamera() as camera:
      # Set camera resolution
      camera.resolution = (320, 240)

      # Get a frame
      stream = io.BytesIO()
      for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
          stream.seek(0)
          frame =  stream.read() 
          email = Email(FROM_ADDRESS, 
                         TO_ADDRESS, 
                         "Test subject", 
                         "Test message", 
                          frame)
          email.send(MAIL_USER, MAIL_PASSWORD)
