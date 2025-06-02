import json
import asyncio # 导入 asyncio 模块
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import BaseMessage

load_dotenv()


client = MultiServerMCPClient(
    {
        "weather": {
            "url": "http://localhost:8083/mcp",
            "transport": "streamable_http",
        }
    }
)

# 将异步操作封装到 async 函数中
async def main():
    tools = await client.get_tools()

    model = ChatTongyi(
        model="qwen2.5-coder-3b-instruct",
        temperature=0,
        verbose=True,
    )

    agent = create_react_agent(
        model=model,
        tools=tools
    )

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in sf?"}]}
    )

    # 自定义序列化函数，用于处理 BaseMessage 类型的对象
    def serialize_message_object(obj):
        if isinstance(obj, BaseMessage):
            return obj.model_dump() # 将消息对象转换为字典
        # 对于其他无法序列化的类型，可以抛出原始错误或返回其字符串表示形式
        # raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
        return str(obj) # 或者返回字符串表示，避免程序中断

    # 使用自定义序列化函数打印结果
    print(json.dumps(weather_response, default=serialize_message_object, indent=2, ensure_ascii=False))

# 使用 asyncio.run() 来运行 async 函数
if __name__ == "__main__":
    asyncio.run(main())