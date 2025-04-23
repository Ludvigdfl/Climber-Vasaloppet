import requests
import base64
import os
import datetime
import time
import json
from openai import OpenAI

###################################################
###############   Helper Functions  ###############
###################################################

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
    File_Type    =  FileName.split('.')[-1]
    BRANCH       = "main"   
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{File_Name}"
 
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)

    content_as_base64 = response.json()['content']

    if File_Type == 'txt':
        content = base64.b64decode(content_as_base64).decode()
    if File_Type == 'json':
        content = json.loads(base64.b64decode(content_as_base64).decode())
    
    return content

def Write_File(FileName, FileContent, TOKEN):

    REPO_OWNER   = "Ludvigdfl"
    REPO_NAME    = "Climber-Vasaloppet"
    File_Name    =  FileName
    File_Type    =  FileName.split('.')[-1]
    BRANCH       = "main"   

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{File_Name}"
 
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)


    if File_Type == 'txt':
        encoded = base64.b64encode(FileContent.encode()).decode()
    if File_Type == 'json':
        encoded = base64.b64encode(json.dumps(FileContent).encode()).decode()
        
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



###################################################
###############   Transform Functions  ############
###################################################

def Call_API(Frames, CLIENT, TOKEN):

    Frames_Added = []
    for index, Frame in enumerate(Frames):

        Prompt = f"""
            You are an expert ski-race tv-host.

            I will send you pairs of images/snapshots from the same race (the swedish ski-race Vasaloppet - A 90 kilometer ski race) 
            Both images are captured at the same time and are thus meant to complement each other. 

            The images comes from the full sequence of images building up the entire. 
            
            To get a smooth and natural flow of commentary, your are also going to be shown the commentary up intil the very last snapshot prior the this one. 
            Take this into account when commenting the current snapshots.
            
            INSTRUCTIONS:
            * 24 words max.
            * Take the prior commentaries into account.
            * Refer to the Underlying data if you think they matter. Just like a tv-host would.
            * Don't make stuff up.
            * Don't use shorts as km, km/h - use Kilometers and Kilometers per hour.

            This is the last 5 Comments from the sequence:
            {Get_History(Frames_Added[-5:])}
            
            * Now mix your style of commenting - i.e. don't use the same structure for each comment - e.g. by ending each comment the same stylish way e.g. with some exclemation like ... exciting race! or...Intersting dynamics! or .. strategies unfolding..!
            * If the same person leads as seen in the previous commentary, one nice stylish comment would thus be to just say that skier X keeps his lead. Not rambeling all skiers one more time.
        """



        response = CLIENT.chat.completions.create(
            
            model="gpt-4o",
            
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": Prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"https://raw.githubusercontent.com/Ludvigdfl/Climber-Vasaloppet/refs/heads/main/Data_Bilder/Data_{Frame['Frame']}.png",
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"https://raw.githubusercontent.com/Ludvigdfl/Climber-Vasaloppet/refs/heads/main/Karta_Bilder/Karta_{Frame['Frame']}.png",
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        Frames_Added.append(
            {
                "Frame" : Frame["Frame"], 
                "Frame_Commentary" : response.choices[0].message.content
            }
        )
        
    Write_File(r"Scripts/Commentary.json", Frames_Added, TOKEN)




def Get_History(Frames):

    History = ''

    if(len(Frames) < 1):
        History  = """
            ***************************************************************    
            THIS IS THE FIRST SNAPSHOT OF THE RACE 
            Thus say something enhancing that, like, .... and they are off!
            ***************************************************************
        """
    for index, Frame in enumerate(Frames):
        History += f"\n\nSnapshot {index}: \n{Frame['Frame_Commentary']}"

    return History



def Get_Final_Transcript(TOKEN):

    Frames = Read_File(r"Scripts/Commentary.json", TOKEN)
    
    Commentary=''
    for Frame in Frames:
        Commentary += f"\n\n{Frame['Frame_Commentary']}" 

    Write_File(r"Scripts/Commentary.txt", Commentary, TOKEN)

    return Commentary
    


def Get_Final_Transcript_Adjusted(CLIENT, TOKEN):

    Prompt = f"""
            You are an expert ski-race tv-host.

            This the transript of a ski-race called vasaloppet.
            Each row corresponds to a time-slice of the race - i.e. the number of words equals a fixed number of seconds.

            However, each row, or each comment, is too similar in style. A real commentator would alternate some more.
            E.g. by not ending each comment with an exclemation ... exciting race! or...Intersting dynamics!

            Here is the full transcript.
            Now adjust and return nothingn but the script WITHOUT modiying the lenght of the script - remember that the lenght corresponds to actual timeslices of the race.
            
            TRANSCRIPT:
            {Get_Final_Transcript(TOKEN)}
            
        """
    response = CLIENT.chat.completions.create(
            
            model="gpt-4o",
            
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": Prompt,
                        }
                    ],
                }
            ] 
    )

    Commentary_Adjusted = response.choices[0].message.content

    Write_File(r"Scripts/Commentary_Adjusted.txt", Commentary_Adjusted, TOKEN)

    return Commentary_Adjusted
        

  

def Generate_And_Store_Voice_Elevenlabs(TRANSCRIPT, TOKEN, YEAR):

    url = "https://api.elevenlabs.io/v1/text-to-speech/gnPxliFHTp6OK6tcoA6i"
    params = {
        "output_format": "mp3_44100_128"
    }
    headers = {
        "xi-api-key": "sk_27d90cbdc065f1a1cc3ff8fb8f5c0c18f9089514b7230c3a",
        "Content-Type": "application/json"
    }
    data = {
        "text": f"{TRANSCRIPT}",
        "model_id": "eleven_multilingual_v2",
        "voice_id": "gnPxliFHTp6OK6tcoA6i"
    }
    
    response = requests.post(url, params=params, headers=headers, json=data)
    AUDIO_PATH = f"Audio_File_{YEAR}.mp3" #f"Audio_File_{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')}.mp3"
    
    if response.status_code == 200:
        with open(AUDIO_PATH , "wb") as f:
            f.write(response.content)
        print(f"Audio saved as {AUDIO_PATH}")
    else:
        print(f"Error: {response.status_code}, {response.text}")


    REPO_OWNER = "Ludvigdfl"
    REPO_NAME = "Climber-Vasaloppet"
    GITHUB_AUDIO = f"Audio_File_{YEAR}.mp3" #f"Audio_File_{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')}.mp3"
    BRANCH = "main"   
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/Audio/{GITHUB_AUDIO}"
    
    # Read and encode the audio file
    with open(GITHUB_AUDIO, "rb") as file:
        audio_content = base64.b64encode(file.read()).decode("utf-8")
    
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




###################################################
###############          MAIN        ##############
###################################################
def main():
    
    TOKEN, OPEN_AI_API = Get_Tokens()
    
    # CLIENT = OpenAI(api_key = OPEN_AI_API)
    
    # Total_Frames = Read_File(r"Scripts/Run_Complete.txt", TOKEN)
    # Frame_Chunks = int(int(Total_Frames)/8)
    # Frames       = [{"Frame" : F_C*8, "Frame_Commentary" : ""} for F_C in range(1,Frame_Chunks+1)]

    # Call_API(Frames, CLIENT, TOKEN)
    
    TRANSCRIPT = Get_Final_Transcript(TOKEN)
    # Get_Final_Transcript_Adjusted(CLIENT, TOKEN) 

    Generate_And_Store_Voice_Elevenlabs(TRANSCRIPT, TOKEN)


main()


 
