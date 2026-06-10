import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_all_paginated_users(endpoint_url):
    """Fetches all users from a paginated GitHub API endpoint."""
    users = set()
    page = 1
    
    while True:
        url = f"{endpoint_url}?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"API Error ({response.status_code}): {response.json()}")
            break
            
        data = response.json()
        if not data:
            break
            
        for user in data:
            users.add(user['login'])
            
        page += 1
        
    return users

def follow_user(target_username):
    """Sends a PUT request to follow a target user."""
    url = f"https://api.github.com/user/following/{target_username}"
    response = requests.put(url, headers=HEADERS)
    
    # HTTP 204 No Content means the follow was successful
    return response.status_code == 204
