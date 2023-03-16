import argparse
from typing import List

import requests
from pydantic import BaseModel


class RequestBody(BaseModel):
    text: List[str]
    lang: str


# Parse command-line arguments using argparse
parser = argparse.ArgumentParser()
parser.add_argument('url', type=str, help='API endpoint URL')
parser.add_argument('text', type=str, nargs='+', help='Text to send in the request')
args = parser.parse_args()

# Set the auth token
auth_token = 'read_from_env_kekw'

# Create the request body using the RequestBody model
request_body = RequestBody(text=args.text, lang="ar")

# Send the request
response = requests.post(args.url, json=request_body.dict(),
                         headers={'auth-token': auth_token, 'Content-Type': 'application/json'})

# Print the response status code and content
print(f'Response status code: {response.status_code}')
print(f'Response content: {response.content}')
