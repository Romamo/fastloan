from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from swarm import Swarm
from assistant.agents import *

app = FastAPI()
client = Swarm()
# agents = Agents()
#
# agents = {
#     "info": InfoAgent(),
#     "form": FormAgent(),
# }

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/index.html", StaticFiles(directory="www", html=True), name="static")


class Message(BaseModel):
    text: str


messages_storage = {}
user_agents = {}


@app.post("/chat")
async def chat(message: Message):
    user_id = 1
    messages = messages_storage.get(user_id, [])
    agent = user_agents.get(user_id, info_agent)
    if isinstance(agent, str):
        agent = all_agents[agent]
    messages.append({"role": "user", "content": message.text})
    response = client.run(agent=agent, messages=messages)
    user_agents[user_id] = response.messages[-1]['sender']
    messages.extend(response.messages)
    messages_storage[user_id] = messages
    return {"response": f'[{agent.name}] {response.messages[-1]["content"]}'}
