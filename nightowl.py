import cv2
import numpy as np
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

'''Developed by Michael Hawes'''
# The program may not recognize faces in certain light levels


# Create funtion to take in arguments to send data through sms. send
# that data to 'list'
def send_mail(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)

# build server in which the message will be sent to and how to attach the vide(text)
    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg.attach(MIMEText(text))

# attch the file to application
    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="output.avi"',
                Name=basename(f)
            ))
# choose the type of email and import the host's server data
# add your email, password
# this allows the program to know who to send the email too and what email to log into
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login('hawes1776@gmail.com','moto4life')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

# create condition statement to show as reference of password login
password = 'correct_password'
user_input = input('Enter a password ')
if user_input == password:
    print("You've been authenticated!")
else:
    print('Authenticating...')

# import the haarfile from intels open source code ( this is what allows the
# program to use facial recognition).
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# enable the video camera on your computer
# the 0 represents your computers camera
# a 1 would be a usb port webcam
    cap = cv2.VideoCapture(0)
# set the count of faces to 0
    count = 0
# set video file to correct type
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
# numbers represent frames per second and resulution
    out = cv2.VideoWriter('output.avi',fourcc, 6.0, (1280,720))
# create a condtion statement to enable the computer to store the videos data
    while cap.isOpened():
        ret, img = cap.read()
# this is the color of the video and the size and color of the
# facial recognition box
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w, y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
# this shows the video live if wanted, I commented this out because the purpose is
# to have the thief not see himself being recorded
        #cv2.imshow('output',img)

# wrtie the video file allowing it to be sendable
        out.write(img)
        
# this prints the number of faces(count)
        #print("Number of faces:", len(faces))
# condition statement to allow the computer to know when to stop the program
# and send the file
        if len(faces) > 0:
            count += 1
# this condition tells the computer where to send the file to
            if count >= 75:
                out.release()
                send_mail('hawes1776@gmail.com', ['mhawes24@gmail.com'], 'subject', 'helloo', files=['output.avi'])
                break
# set the waitkey
        k = cv2.waitKey(10)
        if k == 27:
            break
    #print('(:')
# enable releases adn destroy windows to conclude and end program

    out.release()
    cv2.destroyAllWindows()
