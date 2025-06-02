import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_community.chat_models.tongyi import ChatTongyi 

load_dotenv()

model = ChatTongyi(
    model="qwen2.5-coder-3b-instruct",
    temperature=0,
    verbose=True,
)

agent = create_react_agent(
    model=model,
    tools=[]
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
print(response)