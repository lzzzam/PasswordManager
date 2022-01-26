import io
import os
import os.path
from tkinter import *

from passGenerator import randPass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 
          'https://www.googleapis.com/auth/drive']

ROOT_PATH = os.path.dirname(__file__)
IMG_PATH = os.path.realpath(os.path.join(ROOT_PATH, '..', 'img', 'Lock.gif'))
KEY_DIR_PATH = os.path.realpath(os.path.join(ROOT_PATH, '..', 'key'))
KEY_CSV_PATH = os.path.join(KEY_DIR_PATH, 'keys.csv')

# Google API credentials
creds = None
service = None

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
    
def authorFlow():    
    global creds
    global service
    
    if os.path.exists('key/author/token.json'):
        creds = Credentials.from_authorized_user_file('key/author/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'key/author/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('key/author/token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('drive', 'v3', credentials=creds)
            
def listFiles():
    try:
        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

def syncOnGoogleDrive():
    global creds
    file_id = "1NCtC_jWnHptoyuVsUKQM_B6wL5Jw_iEM"
    authorFlow()
    listFiles()
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    
    print(fh.getvalue())
    # print(f"\n\ntype is {type(content)}\n\n")
    # print(fh)
    # fh.close()
    
    
        
        
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
add.place(x = 100, y = 280)

sync = Button(text = "sync ⇅", width=5, command = syncOnGoogleDrive)
sync.place(x = 265, y = 280)

window.wm_protocol("WM_DELETE_WINDOW", closeProgram)

window.mainloop()