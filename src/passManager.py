import io
import os
import os.path
from tkinter import *
from tkinter import messagebox
import json

from passGenerator import randPass
from googleDriveAPI import getCreds, buildGoogleDriveAPIclient, syncDatabase, updateDatabase
from googleDriveAPI import DATABASE_FILE, DATABASE_DIR, DATABASE_PATH


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 
          'https://www.googleapis.com/auth/drive']

ROOT_PATH = os.path.dirname(__file__)
IMG_PATH = os.path.realpath(os.path.join(ROOT_PATH, '..', 'img', 'Lock.gif'))
IMG_DRIVE_PATH = os.path.realpath(os.path.join(ROOT_PATH, '..', 'img', 'Drive.gif'))
IMG_DRIVE_OK_PATH = os.path.realpath(os.path.join(ROOT_PATH, '..', 'img', 'Drive_Ok.gif'))
IMG_DRIVE_NOT_OK_PATH = os.path.realpath(os.path.join(ROOT_PATH, '..', 'img', 'Drive_NotOk.gif'))

# True when syncronization is established
SYNC_WITH_GOOGLE_DRIVE = False

if not os.path.isdir(DATABASE_DIR):
    os.mkdir(DATABASE_DIR)

def syncToGoogleDrive():
    
    global SYNC_WITH_GOOGLE_DRIVE
    
    if(SYNC_WITH_GOOGLE_DRIVE == False):
        if(messagebox.askyesno("Sync with Drive", 
                               "Syncronize with Google Drive?\nATTENTION: Some of your local password could be lost"
                               )):

            try:
                # Google API credentials
                creds = getCreds()
                # Google API client
                buildGoogleDriveAPIclient(creds)
                syncDatabase()
                SYNC_WITH_GOOGLE_DRIVE = True
                sync.config(text="sync ⇅")
                canvas.itemconfig(drive_img, image = drive_ok)
            except:
                canvas.itemconfig(drive_img, image = drive_notok)
                messagebox.showinfo("Error: Drive", "Error connecting to Google Drive!")
    else:
        
        canvas.itemconfig(drive_img, image = drive)
        sync.config(text="sync")
        SYNC_WITH_GOOGLE_DRIVE = False
                    

def generatePass():
    pwd = randPass(10)
    key_entry.delete(0,"end")
    key_entry.insert(0, pwd)

def addNewPass():
    website = link_entry.get()
    email = email_entry.get()
    pwd = key_entry.get()
    
    if(website == "" or email == "" or pwd == ""):
        messagebox.showinfo("Error: Missing values", "Please, fill all the fields and retry!!")
    else:   
        # load database from .json
        db = None
        with open(DATABASE_PATH, "r+") as fh:
            try:
                db = json.load(fh)
            except:
                db = {}
        
        # modify and update .json file
        with open(DATABASE_PATH, "w") as fh:
            entry = {website : {"email" : email, "pass": pwd}}
            db.update(entry)
            json.dump(db, fh, indent=4)
        
        # sync on Google Drive 
        if(SYNC_WITH_GOOGLE_DRIVE == True):    
            updateDatabase()
    
         
def closeProgram():
    window.destroy()

window = Tk()
window.config(width = 400, height = 350)
window.title("Password Manager")

canvas = Canvas(window,width = 400, height = 320)
canvas.place(x=0, y=0)

logo = PhotoImage(file = IMG_PATH)
lock_img =canvas.create_image(200,90,image = logo)

drive = PhotoImage(file = IMG_DRIVE_PATH)
drive_ok = PhotoImage(file = IMG_DRIVE_OK_PATH)
drive_notok = PhotoImage(file = IMG_DRIVE_NOT_OK_PATH)
drive_img =canvas.create_image(70,290,image = drive)

canvas.create_text(70,185,text="e-mail", font=("Courier", 14))
email_entry = Entry(window, width=25)
email_entry.place(x = 100, y = 170)

canvas.create_text(75,220,text="link", font=("Courier", 14))
link_entry = Entry(window, width=25)
link_entry.place(x = 100, y = 205)

canvas.create_text(60,255,text="password", font=("Courier", 14))
key_entry = Entry(window, width=17)
key_entry.place(x = 100, y = 240)

Auto = Button(text = "Auto", width=4, command = generatePass)
Auto.place(x = 272, y = 240)

add = Button(text = "Add new password", width=15, command = addNewPass)
add.place(x = 100, y = 280)

sync = Button(text = "sync", width=5, command = syncToGoogleDrive)
sync.place(x = 265, y = 280)

window.wm_protocol("WM_DELETE_WINDOW", closeProgram)

window.mainloop()