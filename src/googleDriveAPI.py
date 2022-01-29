import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 
          'https://www.googleapis.com/auth/drive']

TOKEN_PATH          = 'api/token.json'
CREDENTIALS_PATH    = 'api/credentials.json'

DATABASE_FILE       = 'database.json'
DATABASE_DIR        = 'db'
DATABASE_PATH       = os.path.join(DATABASE_DIR, DATABASE_FILE)

service = None
database = None

def getCreds():
    creds = None
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
    media = MediaFileUpload(DATABASE_PATH)
    database = createFile(DATABASE_FILE, media)
    return database

def updateDatabase():
    media = MediaFileUpload(DATABASE_PATH)
    return updateFile(database["id"], media)

def downloadDatabase():
    resp = service.files().get_media(fileId=database["id"]).execute()
    
    with open(DATABASE_PATH, "w") as db:
        db.writelines(resp.decode('utf-8'))
    
def syncDatabase():
    """
    Search for database in Drive. 
    If it not exists it create a new local database from scratch
    and stores it into Drive, otherwise download it from Drive
    """
    global database
    database = searchFile(DATABASE_FILE)
    
    if(database == None):
        # create local db
        with open(DATABASE_PATH, "w") as db:
            db.close()
        # store it into Drive   
        database = createDatabase()
    else:
        downloadDatabase()