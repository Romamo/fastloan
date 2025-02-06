import copy

import gradio as gr

from swarm import Swarm
from assistant.agents import *

client = Swarm()

user_agents = {}

def random_response(message, history):
    user_id = 1
    messages = copy.copy(history)  # messages_storage.get(user_id, [])
    agent = user_agents.get(user_id, info_agent)
    if isinstance(agent, str):
        agent = all_agents[agent]
    messages.append({"role": "user", "content": message})
    response = client.run(agent=agent, messages=messages)
    user_agents[user_id] = response.messages[-1]['sender']
    messages.extend(response.messages)
    return f'[{agent.name}] {response.messages[-1]["content"]}'

gr.ChatInterface(random_response, type="messages", autofocus=True).queue().launch(root_path="/gradio-demo")
