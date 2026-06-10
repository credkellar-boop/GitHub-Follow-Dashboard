# 📈 GitHub-Follow-Dashboard

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)
![GitHub Actions](https://img.shields.io/badge/build-passing-brightgreen?logo=github-actions)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

A lightweight, serverless Python automation tool for passive GitHub audience synchronization. It safely manages state and API rate limits to auto-follow genuine accounts, prune unfollowers, and dispatch real-time alerts across multiple messaging platforms.

---

## ✨ Features

* **Smart Sync:** Automatically detects new followers and follows them back.
* **Auto-Prune:** Detects users who have unfollowed you and automatically unfollows them in return.
* **Omnichannel Routing:** Broadcasts rich alerts to Discord, Telegram, WhatsApp, and Hootsuite.
* **Defensive API Throttling:** Built-in randomized delays (15-45s) to mimic human interaction and strictly adhere to GitHub's Acceptable Use Policies.
* **Blacklist Support:** Easily block known bots or spam accounts from being auto-followed.
* **Serverless Ready:** Fully configured to run passively via GitHub Actions cron workflows.

---

## 🗂️ Project Structure

```text
GitHub-Follow-Dashboard/
│
├── .github/
│   └── workflows/
│       └── dashboard_sync.yml  # GitHub Actions cron scheduler
│
├── core/
│   ├── __init__.py             # Module exports
│   ├── github_api.py           # Core REST API interactions (Follow/Unfollow)
│   └── notifications.py        # Omnichannel webhook dispatcher
│
├── data/                       # State management (Gitignored)
│   ├── blacklist.json          # Array of usernames to ignore
│   └── followers.json          # Cached snapshot of current network
│
├── .env                        # Secure environment variables
├── .gitignore                  # Security and cache exclusions
├── main.py                     # Primary execution loop
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
