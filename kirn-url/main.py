from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.database import Database
import os
import json
import requests

client = Client()

(client
 # Your API Endpoint
 .set_endpoint(os.environ.get('API_ENDPOINT'))
 .set_project(os.environ.get('PROJECT_ID'))  # Your project ID
 .set_key(os.environ.get('API_KEY'))  # Your secret API key
 .set_self_signed()
 )

payload = json.loads(os.environ.get("APPWRITE_FUNCTION_DATA"))
course_name = payload['courseName']
guild_id = payload['guildId']

database = Database(client)

filters = ['userId=' + os.environ.get("APPWRITE_FUNCTION_USER_ID")]

try:
    result = database.list_documents(os.environ.get(
        'COLLECTION_ID'), filters=filters)
    discord_id = result['documents'][0]['discordId']
    data = {
        'guildId': str(guild_id),
        'courseName': str(course_name),
        'userId': str(discord_id)
    }
    data = json.dumps(data)
    request = requests.post(os.environ.get('BOT_API_URL'),
                            headers={'Authorization': os.environ.get('BOT_API_TOKEN')}, data=data)
    print(request.content.decode())
except Exception as e:
    print(e)
    print("Internal Server Error")
