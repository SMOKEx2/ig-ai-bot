from flask import Flask, request
import requests, os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"
    
    if request.method == "POST":
        data = request.json
        try:
            for entry in data["entry"]:
                for msg in entry.get("messaging", []):
                    if "message" in msg:
                        sender_id = msg["sender"]["id"]
                        text = msg["message"].get("text")

                        reply = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "คุณคือแฟนหนุ่มที่คอยตอบแชทอย่างน่ารัก"},
                                {"role": "user", "content": text}
                            ]
                        ).choices[0].message.content

                        send_message(sender_id, reply)
        except Exception as e:
            print("Error:", e)
        return "ok"

def send_message(sender_id, text):
    url = f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": text}
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
