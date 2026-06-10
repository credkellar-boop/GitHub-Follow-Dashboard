import os
import time
import random
import json
from datetime import datetime
from dotenv import load_dotenv

# Import our custom modular components (now including unfollow_user)
from core import get_all_paginated_users, follow_user, unfollow_user, broadcast_alert

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
    
    os.makedirs("data", exist_ok=True)
    
    # 1. Fetch live data
    current_followers = get_all_paginated_users(f"https://api.github.com/users/{USERNAME}/followers")
    current_following = get_all_paginated_users(f"https://api.github.com/users/{USERNAME}/following")
    
    # 2. Load cached local states
    previous_followers = load_json_list(STATE_FILE)
    blacklist = load_json_list(BLACKLIST_FILE)
    
    # 3. Diff tracking: Identify new audience members AND unfollowers
    new_followers = current_followers - previous_followers
    
    # If previous_followers is empty (first run), don't mass-unfollow everyone
    unfollowers = previous_followers - current_followers if previous_followers else set()
    
    if not new_followers and not unfollowers:
        print("No changes detected. Dashboard up to date.")
    
    # --- HANDLE NEW FOLLOWERS ---
    for follower in new_followers:
        if follower in blacklist:
            print(f"Ignored {follower} (on blacklist).")
            broadcast_alert(follower, "Ignored (Blacklisted) 🚫")
            continue
            
        if follower not in current_following:
            print(f"Attempting to follow back: {follower}...")
            success = follow_user(follower)
            
            if success:
                print(f"Successfully followed back {follower}.")
                broadcast_alert(follower, "Followed Back ✅")
            else:
                print(f"Failed to follow {follower}.")
                broadcast_alert(follower, "Failed to Follow ❌")
            
            delay = random.randint(15, 45)
            time.sleep(delay)
        else:
            broadcast_alert(follower, "Already Following 🤝")

    # --- HANDLE UNFOLLOWERS ---
    for unfollower in unfollowers:
        if unfollower in current_following:
            print(f"User {unfollower} unfollowed. Attempting to auto-unfollow...")
            success = unfollow_user(unfollower)
            
            if success:
                print(f"Successfully unfollowed {unfollower}.")
                broadcast_alert(unfollower, "Auto-Unfollowed 💔")
            else:
                print(f"Failed to unfollow {unfollower}.")
                broadcast_alert(unfollower, "Failed to Unfollow ⚠️")
            
            # Throttling to protect the API token
            delay = random.randint(15, 45)
            time.sleep(delay)
                
    # 4. Save state for next cron iteration
    with open(STATE_FILE, "w") as f:
        json.dump(list(current_followers), f, indent=4)
        
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sync complete. State saved.")

if __name__ == "__main__":
    main()
