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
REPO_NAME = "Climber-Podcast"
TEXT_FILE = "Run_Text.txt"   
BRANCH = "main"


##############################################
### 1. Get text file to create speach from ###
##############################################

url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/Scripts/{TEXT_FILE}"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

resp = response.json()
text_endcoded = resp["content"]
decoded_bytes = base64.b64decode(text_endcoded) 
 
TEXT = decoded_bytes.decode("utf-8")
print("TEXT to genereate speach for:\n", TEXT)


###################################################
### 2. Send the TEXT to Elevenlabs to get Audio ###
###################################################

url = "https://api.elevenlabs.io/v1/text-to-speech/pqHfZKP75CvOlQylNhV4"
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
AUDIO_PATH = f"Audio_File_{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')}.mp3"


####################################
### 3. Store the Audio to a file ###
####################################

if response.status_code == 200:
    with open(AUDIO_PATH , "wb") as f:
        f.write(response.content)
    print(f"Audio saved as {AUDIO_PATH}")
else:
    print(f"Error: {response.status_code}, {response.text}")


########################################
### 4. Push the Audio file to Github ###
########################################

REPO_OWNER = "Ludvigdfl"
REPO_NAME = "Climber-Podcast"
GITHUB_AUDIO = f"Audio_File_{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')}.mp3"
BRANCH = "main"   

url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/Audio/{GITHUB_AUDIO}"

# Read and encode the audio file
with open(GITHUB_AUDIO, "rb") as img_file:
    audio_content = base64.b64encode(img_file.read()).decode("utf-8")

# Check if file already exists (needed for updates)
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github.v3+json"}
response = requests.get(url, headers=headers)

# Prepare data for upload
data = {
    "message": "Upload audio via GitHub Actions",
    "content": audio_content,
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
