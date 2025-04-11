import requests
import sys
from typing import List
from dotenv import load_dotenv
import os

# === Load environment variables ===
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MIN_BALANCE = float(os.getenv("MIN_BALANCE", "10"))
NETWORK = os.getenv("NETWORK", "flare").lower()

# === Parse the address list from .env ===
RAW_ADDRESSES = os.getenv("WALLET_ADDRESSES", "")
ADDRESSES = [addr.strip() for addr in RAW_ADDRESSES.split(",") if addr.strip()]

def get_explorer_url(network: str) -> str:
    if network == "flare":
        return "https://flare-explorer.flare.network"
    elif network == "songbird":
        return "https://songbird-explorer.flare.network"
    else:
        raise ValueError("Invalid network. Use 'flare' or 'songbird'.")

# === Get wallet balance from explorer API ===
def get_balance(network: str, address: str) -> float:
    base_url = get_explorer_url(network)
    endpoint = f"{base_url}/api?module=account&action=balance&address={address}"
    try:
        resp = requests.get(endpoint, timeout=10).json()
        if resp.get("status") == "1":
            return int(resp["result"]) / 10**18
        elif resp.get("status") == "0":
            # Address might not exist or be invalid
            return -2
        else:
            return -1
    except Exception as e:
        print(f"Error retrieving balance for {address}: {e}")
        return -1

def send_telegram_alert(message: str):
    print(f"Sending Telegram alert: {message}")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        print("Telegram response:", response.status_code, response.text)
    except Exception as e:
        print(f"Error sending Telegram alert: {e}")


# === Check all addresses and send alerts ===
def check_all_addresses(network: str, addresses: List[str]):
    for address in addresses:
        balance = get_balance(network, address)
        if balance == -1:
            send_telegram_alert(f"❌ *Error* retrieving balance for `{address}` (request error)")
        elif balance == -2:
            send_telegram_alert(f"❗ *Invalid or non-existent address:* `{address}`")
        elif balance < MIN_BALANCE:
            send_telegram_alert(
                f"⚠️ `{address}` has only *{balance:.4f}* {network.upper()} (threshold: {MIN_BALANCE})"
            )
        else:
            print(f"{address} OK: {balance:.4f} {network.upper()}")

# === Main entry point ===
if __name__ == "__main__":
    try:
        check_all_addresses(NETWORK, ADDRESSES)
    except Exception as err:
        send_telegram_alert(f"❌ General error in the script: {err}")
        sys.exit(1)
# send_telegram_alert("✅ *This is a test alert from the script.*")
# This is a test alert from the script.
