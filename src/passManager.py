import os
from tkinter import *

ROOT_PATH = os.path.dirname(__file__)
IMG_PATH = os.path.realpath(os.path.join(ROOT_PATH, '..', 'img', 'Lock.gif'))

window = Tk()
window.title("Password Manager")

canvas = Canvas(window,width = 300, height = 300)
canvas.grid(column=0, row=0, columnspan=4, rowspan=4)

logo = PhotoImage(file = IMG_PATH)
lock_img =canvas.create_image(150,100,image = logo)

window.mainloop()