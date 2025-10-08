from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# CORS setup for your front-end
origins = ["*"]  # agar specific origin hai to ["http://127.0.0.1:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face API key
HF_API_KEY = "YOUR_HUGGINGFACE_API_KEY"
HF_MODEL = "gpt2"  # free model, chaaho to "EleutherAI/gpt-j-6B" ya "bigscience/bloom" bhi use kar sakte ho
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    
    try:
        payload = {"inputs": message}
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
        res_json = response.json()

        # Hugging Face model response parsing
        if "error" in res_json:
            reply = "AI model is busy or unavailable."
        else:
            reply = res_json[0]["generated_text"]

    except Exception as e:
        reply = "Sorry, AI is not available."
        print("Error:", e)

    return {"reply": reply}
