import os
from passGenerator import randPass
from tkinter import *

ROOT_PATH = os.path.dirname(__file__)
IMG_PATH = os.path.realpath(os.path.join(ROOT_PATH, '..', 'img', 'Lock.gif'))
KEY_DIR_PATH = os.path.realpath(os.path.join(ROOT_PATH, '..', 'key'))
KEY_CSV_PATH = os.path.join(KEY_DIR_PATH, 'keys.csv')

if not os.path.isdir(KEY_DIR_PATH):
    os.mkdir(KEY_DIR_PATH)
    
f = open(KEY_CSV_PATH, "a+")

def generatePass():
    pwd = randPass(10)
    key_entry.delete(0,"end")
    key_entry.insert(0, pwd)
    pass

def addNewPass():
    website = link_entry.get()
    email = email_entry.get()
    pwd = key_entry.get()
    f.write(f"{website},{email},{pwd}\n")

def closeProgram():
    f.close()
    window.destroy()

window = Tk()
window.config(width = 400, height = 330)
window.title("Password Manager")

canvas = Canvas(window,width = 400, height = 300)
canvas.place(x=0, y=0)

logo = PhotoImage(file = IMG_PATH)
lock_img =canvas.create_image(200,90,image = logo)

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
add.place(x = 120, y = 280)

window.wm_protocol("WM_DELETE_WINDOW", closeProgram)

window.mainloop()