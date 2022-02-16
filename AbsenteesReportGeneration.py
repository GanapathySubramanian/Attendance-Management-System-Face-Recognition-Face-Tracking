import csv
import os
import datetime
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

# removing present student from studentdetails

list=[]
for i in stuDetails:
    for j in presentstuDetails:
       if((i[0]==j[0])&(i[1]==j[1])&(i[2]==j[2])):
            stuDetails.remove(i)
       else:
            continue

# print(stuDetails)

# to clear unwanted data
absentlist=[]
for i in stuDetails:
    if(i[0]==""):
        continue
    else:
        absentlist.append(i)


# Absentees Report Generation
# try:
#    os.mkdir("../Absentees")
# except OSError as e:
#    print("Directory exists")
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Hour, Minute, Second = timeStamp.split(":")
absentees_file = os.sep+"Absentees_Report_"+date+"_"+Hour+"-"+Minute+"-"+Second

with open("../Absentees/" + absentees_file + ".csv", 'w', newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(header)
    csvwriter.writerows(absentlist)



print("Absentees Report Generated")