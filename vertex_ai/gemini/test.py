from google.oauth2 import service_account
from google.cloud import storage

creds = service_account.Credentials.from_service_account_file(
    r"C:\Users\dharm\Downloads\nimble-root-464019-j7-cba4bb80f715.json"
)

client = storage.Client(credentials=creds, project="nimble-root-464019-j7")
