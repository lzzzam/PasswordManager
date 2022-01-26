import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 
          'https://www.googleapis.com/auth/drive']

TOKEN_PATH          = 'key/author/token.json'
CREDENTIALS_PATH    = 'key/author/credentials.json'

service = None
database = None

def getCreds():
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        
    return creds

def buildGoogleDriveAPIclient(creds):
    global service
    service = build('drive', 'v3', credentials=creds)

def listFiles(pageSize=100):
    global service
    resp =  service.files().list(pageSize=pageSize, fields="files(id, name)").execute()
    return resp.get("files", [])

def searchFile(fileName, pageSize=100):
    files = listFiles(pageSize)
    for file in files:
        if (file["name"] == fileName):
            return file 
    return None

def createFile(fileName, media):
    file_metadata = {'name': fileName}
    return service.files().create(body=file_metadata, media_body=media).execute()

def updateFile(fileId, media):
    return service.files().update(fileId=fileId, media_body=media).execute()    

def createDatabase():
    media = MediaFileUpload('key/keys.csv')
    database = createFile('keys.csv', media)
    return database

def updateDatabase():
    media = MediaFileUpload('key/keys.csv')
    return updateFile(database["id"], media)


creds   = getCreds()
buildGoogleDriveAPIclient(creds)
database = searchFile("keys.csv")
print(database["id"])
updateDatabase()
#print(createDatabase())

