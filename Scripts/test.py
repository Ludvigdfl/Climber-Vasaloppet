import requests
import base64
import os
import datetime
import time
import json

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    print("❌ GitHub TOKEN token not found. Make sure you're running this in GitHub Actions.")
    exit(1)

print(TOKEN)


OPEN_AI_API = os.getenv("OPEN_AI_API")
if not OPEN_AI_API:
    print("❌ GitHub OPEN_AI_API token not found. Make sure you're running this in GitHub Actions.")
    exit(1)

print(OPEN_AI_API)




with open(file=r"Scripts/Commentary.json", mode="r") as File:
    Frames = json.load(File)

Commentary=''
for Frame in Frames:
    Commentary += f'\n\n{Frame["Frame_Commentary"]}'
    
print(Commentary)
