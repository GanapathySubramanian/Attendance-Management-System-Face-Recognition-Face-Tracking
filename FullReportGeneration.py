import csv
import os
import datetime
from queue import Full
import time
date = datetime.date.today().strftime("%B %d, %Y")


# Full Student Details 
path = 'StudentDetails'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-1]
stu_filename = newest
          
# store student details in array
stuDetails = []
with open(stu_filename, 'r') as file:
    csvreader = csv.reader(file)
    headerdetail = next(csvreader)
    for row in csvreader:
        if not row:
            continue
        else:
            stuDetails.append(row)
# print(header)
# print(stuDetails)


# Present student detail
path = '../Attendance'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-1]
presentstu_filename = newest
          

# Full Student Details 
presentstuDetails = []
with open(presentstu_filename, 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        if not row:
            continue
        else:
            presentstuDetails.append(row)


Reportlist=[]
for i in stuDetails:
    if(i[0]==""):
        continue
    else:
        Reportlist.append(i)

for i in Reportlist:
    i.extend(['Absent'])

FullReportlist=[]
for i in Reportlist:
    FullReportlist.append(i)
    for j in presentstuDetails:
       if((i[0]==j[0])&(i[1]==j[1])&(i[2]==j[2])):
          FullReportlist.remove(i)
          i[3]='Present'
          FullReportlist.append(i)
       else:
          continue


# Full Report Generation
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Hour, Minute, Second = timeStamp.split(":")
absentees_file = os.sep+"Full_Attendance_Report_"+date+"_"+Hour+"-"+Minute+"-"+Second

fullreportheader = ['Id', 'Name', 'Email', 'Attendance']

with open("../FullReport/" + absentees_file + ".csv", 'w', newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(fullreportheader)
    csvwriter.writerows(FullReportlist)

print("Full Report Generated")