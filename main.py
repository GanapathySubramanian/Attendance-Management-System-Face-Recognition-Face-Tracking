import os  # accessing the os functions
import check_camera
import Capture_Image
import Train_Image
import Recognize
import RecognizeEyeBlink

# creating the title bar function

def title_bar():
    os.system('cls')  # for windows

    # title of the program

    print("\t\t\t",73 * "*")
    print("\t\t\t",10 * "*" ,"Attendance Management System Using Face Recognition", 10 * "*")
    print("\t\t\t",73 * "*")


# creating the user main menu function

def mainMenu():
    title_bar()
    print()
    print( 10 * "*", "MAIN MENU", 10 * "*")
    print()
    print("[1] Check Camera")
    print("[2] Capture Faces")
    print("[3] Train Images")
    print("[4] Recognize & Attendance")
    print("[5] Eye Blink")
    print("[6] Recognize Face + Eye Blink & Attendance")
    print("[7] Generate Full Report & Sent Mail")
    print("[8] Quit")

    while True:
        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                checkCamera()
                break
            elif choice == 2:
                CaptureFaces()
                break
            elif choice == 3:
                Trainimages()
                break
            elif choice == 4:
                RecognizeFaces()
                break
            elif choice == 5:
                os.system("py EyeBlinkDetector.py")
                break
            elif choice == 6:
                RecognizeFacesDetectEyeBlink()
                break
            elif choice == 7:
                os.system("py AbsenteesReportGeneration.py")
                os.system("py FullReportGeneration.py")
                os.system("py automail.py")
                break
                mainMenu()
            elif choice == 8:
                print("Thank You")
                break
            else:
                print("Invalid Choice. Enter 1-6")
                mainMenu()
        except ValueError:
            print("Invalid Choice. Enter 1-6\n Try Again")
    exit


# ---------------------------------------------------------
# calling the camera test function from check camera.py file

def checkCamera():
    check_camera.camer()
    key = input("Enter any key to return main menu")
    mainMenu()


# --------------------------------------------------------------
# calling the take image function form capture image.py file

def CaptureFaces():
    Capture_Image.takeImages()
    key = input("Enter any key to return main menu")
    mainMenu()


# -----------------------------------------------------------------
# calling the train images from train_images.py file

def Trainimages():
    Train_Image.TrainImages()
    key = input("Enter any key to return main menu")
    mainMenu()


# --------------------------------------------------------------------
# calling the recognize_attendance from recognize.py file

def RecognizeFaces():
    Recognize.recognize_attendence()
    key = input("Enter any key to return main menu")
    mainMenu()

# --------------------------------------------------------------------
# calling the recognize_attendance from recognize&eyeblink.py file

def RecognizeFacesDetectEyeBlink():
    RecognizeEyeBlink.recognize_attendence()
    key = input("Enter any key to return main menu")
    mainMenu()
# ---------------main driver ------------------
mainMenu()
