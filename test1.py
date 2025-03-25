import requests
import base64
import os
import datetime
import time

TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    print("❌ GitHub token not found. Make sure you're running this in GitHub Actions.")
    exit(1)
    
REPO_OWNER = "Ludvigdfl"
REPO_NAME = "Climber-Vasaloppet"
GITHUB_FILE_PATH = "file.txt"  # Path in the repository
BRANCH = "main"

# GitHub API URL
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{GITHUB_FILE_PATH}"

# Prepare headers
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

resp = response.json()
text_endcoded = resp["content"]
decoded_bytes = base64.b64decode(text_endcoded) 
 
TEXT = decoded_bytes.decode("utf-8")

url = "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb"
params = {
    "output_format": "mp3_44100_128"
}
headers = {
    "xi-api-key": "sk_27d90cbdc065f1a1cc3ff8fb8f5c0c18f9089514b7230c3a",
    "Content-Type": "application/json"
}
data = {
    "text": f"{TEXT}",
    "model_id": "eleven_multilingual_v2",
    "voice_id": "pqHfZKP75CvOlQylNhV4"
}


response = requests.post(url, params=params, headers=headers, json=data)
IMAGE_PATH = f"Audio_File_{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')}.mp3"

if response.status_code == 200:
    with open(IMAGE_PATH , "wb") as f:
        f.write(response.content)
    print(f"Audio saved as {IMAGE_PATH}")
else:
    print(f"Error: {response.status_code}, {response.text}")



REPO_OWNER = "Ludvigdfl"
REPO_NAME = "Climber-Vasaloppet"
IMAGE_PATH = "Audio_File_NEW.mp3"
GITHUB_IMAGE_PATH = f"Audio_File_{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')}.mp3"
BRANCH = "main"  # Change if needed

# GitHub API URL
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{GITHUB_IMAGE_PATH}"

# Read and encode the image in Base64
with open(IMAGE_PATH, "rb") as img_file:
    image_content = base64.b64encode(img_file.read()).decode("utf-8")

# Check if file already exists (needed for updates)
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github.v3+json"}
response = requests.get(url, headers=headers)

# Prepare data for upload
data = {
    "message": "Upload image via GitHub Actions",
    "content": image_content,
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
    print("✅ Image successfully uploaded to GitHub!")
else:
    print(f"❌ Failed to upload image: {response.json()}")
