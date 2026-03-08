import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://zooraai.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "online"}

@app.post("/chat")
def chat(data: ChatRequest):
    mensagem = data.message.strip()

    if not mensagem:
        return {"reply": "Envie uma mensagem válida."}

    try:
        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Responda em português, de forma educada e útil."},
                {"role": "user", "content": mensagem}
            ]
        )

        reply = resposta.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Erro ao conectar com a IA: {str(e)}"}