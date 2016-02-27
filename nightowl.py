import cv2
import numpy as np
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def send_mail(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="output.avi"',
                Name=basename(f)
            ))

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login('hawes1776@gmail.com','moto4life')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


password = 'correct_password'
user_input = input('Enter a password ')
if user_input == password:
    print("You've been authenticated!")
else:
    print('Authenticating...')


    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    count = 0
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter('output.avi',fourcc, 8.0, (1280,720))

    while cap.isOpened():
        ret, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w, y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

        #cv2.imshow('output',img)


        out.write(img)



        #print("Number of faces:", len(faces))

        if len(faces) > 0:
            count += 1
            if count >= 75:
                out.release()
                send_mail('hawes1776@gmail.com', ['mhawes24@gmail.com'], 'subject', 'helloo', files=['output.avi'])
                break

        k = cv2.waitKey(10)
        if k == 27:
            break
    #print('(:')
    cap.release()
    out.release()
    cv2.destroyAllWindows()
