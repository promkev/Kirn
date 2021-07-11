from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.database import Database
import os
import json
import requests

client = Client()

(client
 # Your API Endpoint
 .set_endpoint('https://appwrite.grypr.cf/v1')
 .set_project(os.environ.get('PROJECT_ID'))  # Your project ID
 .set_key(os.environ.get('API_KEY'))  # Your secret API key
 )

payload = json.loads(os.environ.get("APPWRITE_FUNCTION_EVENT_DATA"))

provider_token = payload['providerToken']
user_id = payload['userId']

request = requests.get('https://discordapp.com/api/users/@me',
                       headers={'Authorization': 'Bearer ' + provider_token})

discord_id = json.loads(request.content)['id']

database = Database(client)

filters = ['discordId=' + discord_id]

try:
    result = database.list_documents(os.environ.get(
        'COLLECTION_ID'), filters=filters)
    if (result['documents'] == []):
        result = database.create_document(os.environ.get(
            'COLLECTION_ID'), {'userId': user_id, 'discordId': discord_id})
except Exception as e:
    print(e)
    result = database.create_document(os.environ.get(
        'COLLECTION_ID'), {'userId': user_id, 'discordId': discord_id})
