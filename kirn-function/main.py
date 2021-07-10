from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.database import Database
import os
import json
import requests

client = Client()

(client
 .set_endpoint(os.environ.get('API_ENDPOINT'))  # Your API Endpoint
 .set_project(os.environ.get('PROJECT_ID'))  # Your project ID
 .set_key(os.environ.get('API_KEY'))  # Your secret API key
 )

payload = json.loads(os.environ["APPWRITE_FUNCTION_EVENT_DATA"])
provider_token = payload['providerToken']

response = requests.get('https://discordapp.com/api/users/@me',
                        headers={'Authorization': 'Bearer ' + provider_token})

discordId = response['id']

database = Database(client)

try:
    result = database.list_documents(os.environ.get(
        'COLLECTION_ID'), filters='discordId=' + discordId)
except:
    result = database.create_document(os.environ.get(
        'COLLECTION_ID'), {'discordId': discordId})
