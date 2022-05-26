import datetime
from operator import truediv
import os
import time
from traceback import print_tb
import yagmail
import cv2
import pandas as pd


#-------------------------
def recognize_attendence():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("./TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")
    
    first_read = True
    eye_blink_count=0;
    att_stu=[];
    # attendance_taken=False;

    df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name','Email','Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        _,im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        gray_scale = cv2.bilateralFilter(gray, 5, 1, 1)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
        for(x, y, w, h) in faces:
            image=cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            # eye_face var will be i/p to eye classifier
            eye_face = gray_scale[y:y + h, x:x + w]
            # image
            eye_face_clr = image[y:y + h, x:x + w]
            # get the eyes
            eyes = eyes_cascade.detectMultiScale(eye_face, 1.3, 5, minSize=(50, 50))
            for(ex,ey,ew,eh) in eyes:
                cv2.rectangle(eye_face_clr,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
           
            if conf < 100:
                aa = df.loc[df['Id'] == Id]['Name'].values
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id)+"-"+aa
                e_id=df.loc[df['Id'] == Id]['Email'].values
            else:
                Id = '  Unknown  '
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))
                
            # if (100-conf) > 60:
            #     ts = time.time()
            #     date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            #     timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            #     aa = str(aa)[2:-2]
            #     email=str(e_id)[2:-2]
            #     if eye_blink_count>=20:
            #         attendance.loc[len(attendance)] = [Id, aa,email,date, timeStamp]
            
            tt = str(tt)[2:-2]
            if(100-conf) > 60:
                tt = tt + " [Pass]"
                cv2.putText(im, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2) 
                if len(eyes) >= 2:
                    if first_read:
                        cv2.putText(image, "Eye's detected press 's' to start or 'q' to quit", (10, 80), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)
                    else:
                        cv2.putText(image, "Eye's Open", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)
                else:
                    if first_read:
                        cv2.putText(image, "No Eye's detected", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 255, 255), 2)
                    else:
                        cv2.putText(image, "Blink Detected.....!!!!", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 255, 0), 2)
                        eye_blink_count=eye_blink_count+1;
                if(eye_blink_count>=20):                    
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = str(aa)[2:-2]
                    email=str(e_id)[2:-2]
                    attendance.loc[len(attendance)] = [Id, aa,email,date, timeStamp]
                    if str(Id) in att_stu:
                        print("attendance taken for "+aa+ " Please Move")
                        # attendance_taken=True;
                        # first_read=True
                        eye_blink_count=0
                        continue
                    else:
                        # attendance_taken=False;
                        att_stu.append(str(Id))
            else:
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)


            if (100-conf) > 60:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
            elif (100-conf) > 50:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Attendance', im)
        a = cv2.waitKey(1)
        if a == ord('q'):
            break
        elif a == ord('s'):
           first_read = False
    if(att_stu):
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName, index=False)
        print("Present Student Excel Genrated")
    cam.release()
    cv2.destroyAllWindows()


