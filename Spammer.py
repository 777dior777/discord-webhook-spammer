import requests
import json
import threading
import colorama
from colorama import Fore
import webbrowser

colorama.init(autoreset=True)

def print_ascii_art():
    ascii_art = r"""

 __      __      ___.   .__                   __    
/  \    /  \ ____\_ |__ |  |__   ____   ____ |  | __
\   \/\/   // __ \| __ \|  |  \ /  _ \ /  _ \|  |/ /
 \        /\  ___/| \_\ \   Y  (  <_> |  <_> )    < 
  \__/\  /  \___  >___  /___|  /\____/ \____/|__|_ \
       \/       \/    \/     \/                   \/
 
                                                                          
"""
    print(Fore.GREEN + ascii_art)
    print(Fore.GREEN + "https://discord.com/terms\n")

def read_webhooks_from_config():
    webhooks = []
    try:
        with open("config.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                webhook = line.strip()
                if webhook:
                    webhooks.append(webhook)
    except FileNotFoundError:
        print("Config file not found.")
    return webhooks

def spam_webhook(webhook_url, message, times):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'content': message
    }

    for _ in range(times):
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
        print(Fore.CYAN + f"Sent to Webhook ({message})")

def main():
    print_ascii_art()
    
    webhooks = read_webhooks_from_config()

    if not webhooks:
        print("No webhooks found in config.")
        return

    print(Fore.BLUE + "How many messages do you want to send?")
    num_times = int(input())

    print(Fore.BLUE + "What shall the message be? (Example: '@everyone RAIDED ')")
    message = input()

    threads = []
    for url in webhooks:
        thread = threading.Thread(target=spam_webhook, args=(url, message, num_times))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
