import requests
import json
import os.path
def load_apikey():
    api_key_file = os.path.expanduser('aidevs2.txt')
    if os.path.exists(api_key_file):
        with open(api_key_file, 'r') as file:
            return file.read().strip()
    else:
        raise ValueError("API key file not found")

BASE_URL = 'https://zadania.aidevs.pl'
APIKEY = load_apikey()
TASK = 'moderation'

# STEP 1: Get the token
token_response = requests.post(f'{BASE_URL}/token/{TASK}', json={"apikey": APIKEY})
token_data = json.loads(token_response.text)
token = token_data['token']

# STEP 2: Get the task
task_response = requests.get(f'{BASE_URL}/task/{token}')
task_data = json.loads(task_response.text)
sentences = task_data['input']

# Perform moderation check on the sentences and prepare the answer
moderation_statuses = []

for sentence in sentences:
    moderation_result = json.loads(requests.post('https://api.openai.com/v1/moderations', headers={'Content-Type': 'application/json',
    'Authorization': f'Bearer {APIKEY}'},
    json={'input': sentence}))

    if 'flagged' in moderation_result:
        flagged = moderation_result['flagged']
        moderation_statuses.append(1 if flagged else 0)
    else:
        moderation_statuses.append(0)

# STEP 3: Send the final answer
answer_response = requests.post(f'{BASE_URL}/answer/{token}', json={"answer": json.dumps(moderation_statuses)})
answer_data = json.loads(answer_response.text)
