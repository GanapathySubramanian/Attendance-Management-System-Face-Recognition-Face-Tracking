import csv
import yagmail
import os
import datetime

# mail information
yag = yagmail.SMTP("ganapathydaprojects@gmail.com", "Presidio")

date = datetime.date.today().strftime("%B %d, %Y")

staffEmail="ganapathy5subramanian@gmail.com"

def sendEmail(mailTo,sub,content,attachment_file,msg):
    if(attachment_file==""):
        yag.send(
            to=mailTo,
            subject=sub, # email subject
            contents=content,  # email body
        )
    else:
        yag.send(
            to=mailTo,
            subject=sub, # email subject
            contents=content,  # email body
            attachments=attachment_file  # file attached
        )
    # print(msg)


#Email Sent To Staff - Present Student
path = 'Attendance'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-1]
presentstu_filename = newest
sendEmail(staffEmail,"Attendance Report for " + str(date),"Present Students Report for today class has been attached here kindly check it out",presentstu_filename,"Present student Report Email Sent to the staff")



#Email Sent To Student - Present Student
presentstu_email=[]
name=[]
with open(presentstu_filename,'r')as csv_file:
    csv_reader=csv.reader(csv_file)
    for line in csv_reader:
        presentstu_email=line
        if(line[1]=='Name'):
            continue
        else:
            name=line[1]
        if(presentstu_email[2]=='Email'):
            continue
        else:
            sendEmail(presentstu_email[2],"Attendance Report for " + str(date),"Hello "+name+" Your Attendance for today's class is : Present","","Email sent to the present students")




# Email Sent to staff - Absent Student
path = '../Absentees'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-1]
absentstu_filename = newest
sendEmail(staffEmail,"Attendance Report for " + str(date),"Absent Students Report for today class has been attached here kindly check it out",absentstu_filename,"Absent student Report Email Sent to the staff")



#Email Sent to Student - Absent Student
absentstu_email=[]
absentname=[]
fulldate = datetime.date.today().strftime("%B %d, %Y")
with open(absentstu_filename,'r')as csv_file:
    csv_reader=csv.reader(csv_file)
    for line in csv_reader:
        if(line[0]==''):
            continue
        else:
            absentstu_email=line
        if(line[1]=='Name'):
            continue
        else:
            absentname=line[1]
        if(absentstu_email[2]=='Email'):
            continue
        else:
            sendEmail(absentstu_email[2],"Attendance Report for " + str(date),"Hello "+absentname+" Your Attendance for today's class is : Absent","","Email sent to the absent students")


#Email Sent to staff - Full Report
path = '../FullReport'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-1]
fullreport_filename = newest 
sendEmail("ganapathy5subramanian@gmail.com","Full Attendance Report for " + str(date),"Full Report for today's class has been attached here kindly check it out",fullreport_filename,"Full Report Email Sent to the staff")

print("Email Sent")