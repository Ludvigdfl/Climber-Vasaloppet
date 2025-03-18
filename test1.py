import requests

url = "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb"
params = {
    "output_format": "mp3_44100_128"
}
headers = {
    "xi-api-key": "sk_27d90cbdc065f1a1cc3ff8fb8f5c0c18f9089514b7230c3a",
    "Content-Type": "application/json"
}
data = {
    "text": "The first move is what sets everything in motion.",
    "model_id": "eleven_multilingual_v2"
}


response = requests.post(url, params=params, headers=headers, json=data)
print(response)
if response.status_code == 200:
    with open("output_NEW_2.mp3", "wb") as f:
        f.write(response.content)
    print("Audio saved as output.mp3")
else:
    print(f"Error: {response.status_code}, {response.text}")
