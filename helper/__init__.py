from dotenv import load_dotenv, find_dotenv
import os
import sys

# Define basepath 
base_path = os.path.abspath('..') # this will go one folder back
print('BASE_PATH =', base_path)
sys.path.append(base_path)

dotenv_path = find_dotenv('secrets.env')
print("Path of secrets.env =",dotenv_path)

# Execute .env file
load_dotenv(dotenv_path)

# load environment variables
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
mongodb_conn_str = os.environ.get("MONGODB_CONNECTION_STRING")

# insert username and password
mongodb_connection_string = mongodb_conn_str.format_map(
    {
        'db_username': db_username,
        'db_password': db_password
    }
)

# load openai api keys
openai_api_key = os.environ.get('OPENAI_API_KEY')