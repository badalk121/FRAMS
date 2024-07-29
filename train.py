import tkinter as tk
from tkinter import *
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time


def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text=res)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def TakeImages():
    Id = (txt.get())
    name = (txt2.get())
    if(is_number(Id) and name.isalpha()):
        # if(Id.isalnum() and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "Haarcascade\haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # Incrementing sample number
                sampleNum = sampleNum+1
                # Saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                # display the frame
                cv2.imshow('Capture Window', img)
            # Wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : K" + Id + " Name : " + name
        row = [Id, name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name!"
            message.configure(text=res)
        if(name.isalpha()):
            res = "Enter Numeric Id!"
            message.configure(text=res)


def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "Haarcascade\haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Images Trained."  # +",".join(str(f) for f in Id)
    message.configure(text=res)


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, Recognizer = cam.read()
        gray = cv2.cvtColor(Recognizer, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(Recognizer, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if(conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = 'K'+str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            else:
                Id = 'Unknown'
                tt = str(Id)
            if(conf > 75):
                noOfFile = len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) +
                            ".jpg", Recognizer[y:y+h, x:x+w])
            cv2.putText(Recognizer, str(tt), (x, y+h),
                        font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Attendance Window', Recognizer)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName, index=False)
    cam.release()
    cv2.destroyAllWindows()
    # print(attendance)
    res = attendance
    message2.configure(text=res)


window = tk.Tk()
window.title("F.R.A.M.S")
window.iconbitmap(r'FRAMS.ico')
window.geometry('1200x650')
window.resizable(False, False)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

image = Image.open('background.jpg')
image = image.resize((1200, 650), Image.ANTIALIAS)
my_bg = ImageTk.PhotoImage(image)
my_lbl = Label(image=my_bg)
my_lbl.pack()

message = tk.Label(window, text="Face Recognition based Attendance Management System",
                   bg="#08457e", fg="White", width=50, height=2, font=('times', 22, 'bold'))

message.place(x=200, y=20)

lbl = tk.Label(window, text="Enter ID", width=15, height=2,
               fg="White", bg="#08457e", font=('times', 15, ' bold '))
lbl.place(x=225, y=150)

txt = tk.Entry(window, width=20, bg="#08457e",
               fg="White", font=('times', 18))
txt.place(x=525, y=158)

lbl2 = tk.Label(window, text="Enter Name", width=15, fg="White",
                bg="#08457e", height=2, font=('times', 15, ' bold '))
lbl2.place(x=225, y=250)

txt2 = tk.Entry(window, width=20, bg="#08457e",
                fg="White", font=('times', 18,))
txt2.place(x=525, y=258)

lbl3 = tk.Label(window, text="Status", width=15, fg="White",
                bg="#08457e", height=2, font=('times', 15, ' bold '))
lbl3.place(x=225, y=350)

message = tk.Label(window, text="", bg="#08457e", fg="White", width=40,
                   height=1, activebackground="yellow", font=('times', 15))
message.place(x=525, y=358)

lbl3 = tk.Label(window, text="Attendance List", width=15, fg="White",
                bg="#08457e", height=2, font=('times', 15, ' bold '))
lbl3.place(x=225, y=550)

message2 = tk.Label(window, text="", fg="White", bg="#08457e",
                    activeforeground="green", width=50, height=2, font=('times', 15))
message2.place(x=525, y=550)

clearButton = tk.Button(window, text="Clear", command=clear, fg="White", bg="#08457e",
                        width=6, height=1, activebackground="cyan", font=('times', 12, ' bold '))
clearButton.place(x=810, y=158)
clearButton2 = tk.Button(window, text="Clear", command=clear2, fg="White", bg="#08457e",
                         width=6, height=1, activebackground="cyan", font=('times', 12, ' bold '))
clearButton2.place(x=810, y=258)
takeImg = tk.Button(window, text="Capture Images", command=TakeImages, fg="White",
                    bg="#08457e", width=15, height=2, activebackground="cyan", font=('times', 15, ' bold '))
takeImg.place(x=100, y=450)
trainImg = tk.Button(window, text="Train Images", command=TrainImages, fg="White",
                     bg="#08457e", width=15, height=2, activebackground="cyan", font=('times', 15, ' bold '))
trainImg.place(x=350, y=450)
trackImg = tk.Button(window, text="Start Taking Attendance", command=TrackImages, fg="White",
                     bg="#08457e", width=18, height=2, activebackground="cyan", font=('times', 15, ' bold '))
trackImg.place(x=600, y=450)

quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="White", bg="#08457e",
                       width=15, height=2, activebackground="cyan", font=('times', 15, ' bold '))
quitWindow.place(x=900, y=450)
copyWrite = tk.Text(window, background="#08457e",
                    borderwidth=2, width=10, font=('times', 14, 'italic'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "   FRAMS", "", "©", "subscript")
copyWrite.configure(state="disabled", fg="White")
copyWrite.pack(side="bottom")
copyWrite.place(x=530, y=625)

window.mainloop()
