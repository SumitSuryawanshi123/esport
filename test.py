import requests

# Define the URL of the deployed FastAPI application
api_url = "https://esport-f30e.onrender.com"

# Example data for a POST request
data = {
    "text": """Almost everyone in India knew PUBG through Dynamo and some hates him for no reason. I started playing PUBG after seeing his stream..Hail hydra:
2022 mai kon kon fhirse dekrahan hai purana yando mai:
fantastic game big fan bro from pakistan:
Wahh bete wahh patt se headshot:
Mai apaka bahut bada fan ho. Bhai:
Those days when dynamo use to rule in Indian gaming community:
Hello bhai Damini bhai aapka sabse bada fan Hoon Duniya Ke sabse bada fan:
Mai Apka bahut  bada  fan hoo bro mughe  bhi apne  sath  khilayenge:
Dayno bhai mujhe v aapki support ki jrurat hai:
Bro you play a nice Game.So, I gave you a +Subscribe:
Dynamo Bhai aap bahut hi khatarnak sniping karte Hain:
Bhai jo aapki Video dekh raha hun mobile Nokia ka phone hai bhai:"""
    # If uploading a file, you would add it here as well
}

file_data = {
    "img": ("ebHMYdD.png", open("ebHMYdD.png", "rb"), "image/jpeg")
}

# Make a POST request to the /extract_text/ endpoint
response = requests.post(f"{api_url}/get_sentiment/", data=data)
print(response.json())


response_extraction = requests.post(f"{api_url}/extract_text/", files=file_data)
print("Text Extraction Response:", response_extraction.json())
