import requests
import base64
import os
import datetime
import time
import json


def Get_Tokens():
    
    TOKEN = os.getenv("GITHUB_TOKEN")
    if not TOKEN:
        print("❌ GitHub TOKEN token not found. Make sure you're running this in GitHub Actions.")
        exit(1)
     
    
    OPEN_AI_API = os.getenv("OPEN_AI_API")
    if not OPEN_AI_API:
        print("❌ GitHub OPEN_AI_API token not found. Make sure you're running this in GitHub Actions.")
        exit(1)

    return TOKEN, OPEN_AI_API


def Read_File(FileName, TOKEN):
    REPO_OWNER   = "Ludvigdfl"
    REPO_NAME    = "Climber-Vasaloppet"
    File_Name    =  FileName
    BRANCH       = "main"   
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{File_Name}"
 
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)

    content_as_base64 = response.json()['content']
    content = base64.b64decode(content_as_base64).decode()

    return content

def Write_File(FileName, FileType, FileContent, TOKEN):

    REPO_OWNER   = "Ludvigdfl"
    REPO_NAME    = "Climber-Vasaloppet"
    File_Name    =  FileName
    BRANCH       = "main"   
    
    encoded = base64.b64encode(FileContent.encode()).decode()
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{File_Name}"
 
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    
    # Prepare data for upload
    data = {
        "message": "Upload audio via GitHub Actions",
        "content": encoded,
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



##################################
############## MAIN ##############
def main():
    
    TOKEN, OPEN_AI_API = Get_Tokens()
    
    Write_File(FileName = r"Scripts/Commentary.txt", FileType = "txt", FileContent = "Hej go o gla", TOKEN = TOKEN)

    content = Read_File(FileName = r"Scripts/Commentary.txt",  TOKEN = TOKEN)
    print(content)
    
 
    

main()
