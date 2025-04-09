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
 

OPEN_AI_API = os.getenv("OPEN_AI_API")
if not OPEN_AI_API:
    print("❌ GitHub OPEN_AI_API token not found. Make sure you're running this in GitHub Actions.")
    exit(1)

 
with open(file=r"Scripts/Commentary.json", mode="r") as File:
    Frames = json.load(File)

Commentary=''
for Frame in Frames:
    Commentary += f'\n\n{Frame["Frame_Commentary"]}'
    
print(Commentary)

FILE_TMP  = "Scripts/Commentary_TEMP.txt" 

with open(file= FILE_TMP, mode="w") as File:
    File.write(Commentary)




REPO_OWNER   = "Ludvigdfl"
REPO_NAME    = "Climber-Vasaloppet"
FILE         = "Commentary.txt"
BRANCH       = "main"   

url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/Scripts/{FILE}"

# Read and encode the audio file
with open(FILE_TMP, "r") as File:
    Content_File = File.read()

# Check if file already exists (needed for updates)
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github.v3+json"}
response = requests.get(url, headers=headers)

# Prepare data for upload
data = {
    "message": "Upload audio via GitHub Actions",
    "content": Content_File,
    "branch": BRANCH
}

if response.status_code == 200:
    # File exists, update it
    sha = response.json().get("sha")  # Get the SHA of the existing file
    data["sha"] = sha  # Add SHA to the data for the update
    response = requests.put(url, json=data, headers=headers)
else:
    # File does not exist, create it
    response = requests.put(url, json=data, headers=headers)

# Check response status
if response.status_code in [200, 201]:
    print("✅ Data successfully uploaded to GitHub!")
else:
    print(f"❌ Failed to upload Data: {response.json()}")
