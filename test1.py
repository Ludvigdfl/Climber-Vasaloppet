import requests
import base64
import os


url = "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb"
params = {
    "output_format": "mp3_44100_128"
}
headers = {
    "xi-api-key": "sk_27d90cbdc065f1a1cc3ff8fb8f5c0c18f9089514b7230c3a",
    "Content-Type": "application/json"
}
data = {
    "text": "My name is Ludvig and I am a climber.",
    "model_id": "eleven_multilingual_v2"
}


response = requests.post(url, params=params, headers=headers, json=data)
IMAGE_PATH = "Audio_File.mp3"

if response.status_code == 200:
    with open(IMAGE_PATH , "wb") as f:
        f.write(response.content)
    print("Audio saved as Audio_File2.mp3")
else:
    print(f"Error: {response.status_code}, {response.text}")

 




# GitHub repository details
TOKEN = "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"  # Use a secure method to store your token
TOKEN = "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"
TOKEN = "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"


REPO_OWNER = "Ludvigdfl"
REPO_NAME = "Climber-Vasaloppet"
IMAGE_PATH = IMAGE_PATH # Local path to the image
GITHUB_IMAGE_PATH = "TO_GIT_NEW.mp3"  # Path in the repository
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
