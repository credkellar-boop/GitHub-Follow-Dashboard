import os
import time
import random
import json
from datetime import datetime
from dotenv import load_dotenv

# Import our custom modular components
from core import get_all_paginated_users, follow_user, broadcast_alert

# Load environment variables
load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME")
STATE_FILE = "data/followers.json"
BLACKLIST_FILE = "data/blacklist.json"

def load_json_list(filepath):
    """Safely loads a JSON list from a file."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting GitHub-Follow-Dashboard Sync...")
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # 1. Fetch live data using our core API module
    current_followers = get_all_paginated_users(f"https://api.github.com/users/{USERNAME}/followers")
    current_following = get_all_paginated_users(f"https://api.github.com/users/{USERNAME}/following")
    
    # 2. Load cached local states
    previous_followers = load_json_list(STATE_FILE)
    blacklist = load_json_list(BLACKLIST_FILE)
    
    # 3. Diff tracking: Identify new audience members
    new_followers = current_followers - previous_followers
    
    if not new_followers:
        print("No new followers detected. Dashboard up to date.")
    else:
        for follower in new_followers:
            # Check blacklist safety guardrail
            if follower in blacklist:
                print(f"Ignored {follower} (on blacklist).")
                broadcast_alert(follower, "Ignored (Blacklisted) 🚫")
                continue
                
            # If they follow you but you don't follow them, evaluate follow-back
            if follower not in current_following:
                print(f"Attempting to follow back: {follower}...")
                success = follow_user(follower)
                
                if success:
                    print(f"Successfully followed back {follower}.")
                    broadcast_alert(follower, "Followed Back ✅")
                else:
                    print(f"Failed to follow {follower}.")
                    broadcast_alert(follower, "Failed to Follow ❌")
                
                # Randomized throttling sleep to mimic human interaction pattern
                delay = random.randint(15, 45)
                print(f"Sleeping for {delay}s...")
                time.sleep(delay)
            else:
                # You already follow them, just broadcast the alert
                broadcast_alert(follower, "Already Following 🤝")
                
    # 4. Save state for next cron iteration
    with open(STATE_FILE, "w") as f:
        json.dump(list(current_followers), f, indent=4)
        
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sync complete. State saved.")

if __name__ == "__main__":
    main()
