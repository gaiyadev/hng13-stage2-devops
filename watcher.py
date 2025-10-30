#!/usr/bin/env python3
import os
import time
import requests

print("=== ALERT WATCHER STARTING ===")

SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK_URL')
last_pool = os.getenv('ACTIVE_POOL', 'blue')

print(f"SLACK_WEBHOOK: {bool(SLACK_WEBHOOK)}")
print(f"ACTIVE_POOL: {last_pool}")

def send_slack(msg):
    try:
        response = requests.post(SLACK_WEBHOOK, json={"text": msg}, timeout=5)
        print(f"ALERT SENT: {msg}")
        return True
    except Exception as e:
        print(f"SLACK ERROR: {e}")
        return False

LOG_FILE = '/var/log/nginx/access.log'
while not os.path.exists(LOG_FILE):
    print(f"Waiting for log file: {LOG_FILE}")
    time.sleep(2)

print("Starting to monitor logs...")

processed = set()
while True:
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            if line not in processed:
                processed.add(line)
                
                if 'pool:blue' in line and last_pool != 'blue':
                    send_slack(f"FAILOVER: {last_pool} -> blue")
                    last_pool = 'blue'
                    print(f"Pool changed to: blue")
                
                elif 'pool:green' in line and last_pool != 'green':
                    send_slack(f"FAILOVER: {last_pool} -> green")
                    last_pool = 'green'
                    print(f"Pool changed to: green")
        
        if len(processed) > 1000:
            processed = set(list(processed)[-500:])
            
        time.sleep(2)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)