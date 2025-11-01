import os, time, requests

BLUE = os.getenv("BLUE_URL")
GREEN = os.getenv("GREEN_URL")
SLACK = os.getenv("SLACK_WEBHOOK_URL")

def notify(message):
    if SLACK:
        try:
            requests.post(SLACK, json={"text": message})
        except Exception as e:
            print("Slack notification failed:", e)

def is_alive(url):
    try:
        res = requests.get(url, timeout=2)
        return res.status_code == 200, res.status_code
    except Exception:
        return False, None

blue_up, green_up = True, True
error_count = 0  # 🔹 track repeated errors for high error rate alert

while True:
    b_alive, b_status = is_alive(BLUE)
    g_alive, _ = is_alive(GREEN)

    # --- Failover detection ---
    if not b_alive and blue_up:
        notify("🚨 Blue app DOWN! Failing over to Green!")
        blue_up = False
    elif b_alive and not blue_up:
        notify("✅ Blue app recovered.")
        blue_up = True

    if not g_alive and green_up:
        notify("🚨 Green app DOWN!")
        green_up = False
    elif g_alive and not green_up:
        notify("✅ Green app recovered.")
        green_up = True

    # --- High error rate detection ---
    if b_status and 500 <= b_status < 600:
        error_count += 1
    else:
        error_count = 0

    if error_count >= 3:
        notify("⚠️ High Error Rate detected on Blue app! (3 consecutive 5xx)")
        error_count = 0

    time.sleep(5)
