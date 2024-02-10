from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import PIL.Image
import json

load_dotenv()

app = FastAPI()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response_sentiment(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def get_gemini_response_image(input_prompt,img):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt,img[0]])
    return response.text

# def input_image_setup(upload_file):
#     if upload_file is not None:
#         bytes_data =upload_file.read()
#         return {
#             "mime_type": upload_file.content_type,
#             "data": bytes_data
#         }
#     else:
#         raise FileNotFoundError("No file uploaded")

def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.file.read()
        image_parts = [{
            "mime_type": upload_file.content_type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



sentiment_input_prompt = """
As a sentiment analyzer for live streaming game video chats, your task is to analyze the provided chat text and provide positive and negative scores out of 100. Additionally, you have to suggest improvements that the streamer can implement during future streams based on only the chat feedback (Do not add your own improvements). Each chat text will be separated by a colon (:).

Here is the chat text: {text}

The response will be provided in a single string with the following structure:
{{"positive_score":"%","negative_score":"%","improvements_to_be_done":[]}}
"""

pubg_img_input_prompt = """
    you have extract text from image of game score card and return each line of response in json format (do not add '\' or '\n' in json file)
    
    The response will be provided in a single string with the following structure:
{"Grade:"?","MVP_player_name":"?","Player":[{"Name":"?","kills":"?","damage":"?","survival_time":"?","health_restored":"?"}]}

use above format for all players
"""

valorant_img_input_prompt = """
    you have extract text from image of game score card and return each line of response in json format (do not add '\' or '\n' in json file)
    
    The response will be provided in a single string with the following structure:
{"status_of_lost_or_win:"?","MVP_player_name":"?","Player":[{"Name":"?","avg_combat_score":"?","KDA":"?"}]}

use above format for all players
"""

@app.get("/")
def red_root():
    return "welcome"


@app.post("/get_sentiment/")
async def sentiment(text: str = Form(...)):
    Sentiment_response = get_gemini_response_sentiment(sentiment_input_prompt.format(text=text))
    return json.loads(Sentiment_response)

@app.post("/extract_text/")
async def extract_text(img: UploadFile = File(...),game_name: str = Form(...)):
    new_img = input_image_setup(img)
    if game_name == "PUBG" or game_name == "pubg":
        img_text = get_gemini_response_image(pubg_img_input_prompt,new_img)
    if game_name == "VALORANT" or game_name == "valorant":
        img_text = get_gemini_response_image(valorant_img_input_prompt,new_img)
    return  json.loads(img_text)

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="127.0.0.1", port=8080)


