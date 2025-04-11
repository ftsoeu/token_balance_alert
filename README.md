# 🔔 Flare/Songbird Token Balance Alert Bot

This Python script checks a list of Flare or Songbird wallet addresses and sends a Telegram alert if any wallet has a token balance below a defined threshold.

## 🚀 Features

- Supports both **Flare** and **Songbird** networks.
- Sends alerts via **Telegram Bot**.
- Can be scheduled (e.g., every hour using `cron`).
- Uses a `.env` file to protect secrets and make it GitHub-friendly.

## 🛠 Requirements

- Python 3.7+
- Dependencies: `requests`, `python-dotenv`

```bash
pip install -r requirements.txt
