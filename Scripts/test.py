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
 
def Read_File(File_Name, FileType):

    if(FileType == 'json'):
        with open(file = File_Name, mode="r") as File:
           Data = json.load(File)
            
        return Data
        
    if(FileType == 'txt'):
        with open(file = File_Name, mode="r") as File:
           Data = File.read()
            
        return Data


def Write_File_Tmp(File_Name_TMP, FileType, File_Content):

     if(FileType == 'json'):
        with open(file = File_Name_TMP, mode="r") as File:
           json.dump(File_Content, File_Name_TMP)
            
        return Data
        
    if(FileType == 'txt'):
        with open(file = File_Name_TMP, mode="r") as File:
           File.write(File_Content)
            
        return Data



def Write_File(File_Name, FileType, File_Content, TOKEN):

    REPO_OWNER   = "Ludvigdfl"
    REPO_NAME    = "Climber-Vasaloppet"
    FILE         =  File_Name
    BRANCH       = "main"   
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/Scripts/{FILE}"

    if(FileType == 'txt'):
        with open(FILE_TMP, "rb") as File:
            Content_File = base64.b64encode(File.read()).decode()
     
    else:
        with open(FILE_TMP, "rb") as File:
            Content_File = base64.b64encode(json.load(File).decode()   

                                            
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



##################################
############## MAIN ##############
def main():
    
    TOKEN, OPEN_AI_API = Get_Tokens()

    Content_test = Read_File(FileName = r"Scripts/Commentary.txt", "txt")

    print(Content_test)
    

    

main()
