import os
import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langgraph.prebuilt import create_react_agent
from langchain_openai.chat_models import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

with open("system_prompt.md", "r") as file:
    system_prompt =  file.read()

async def create_agent_with_tools():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    # Create persistent stdio client and session
    stdio_ctx = stdio_client(server_params)
    read, write = await stdio_ctx.__aenter__()
    
    session_ctx = ClientSession(read, write)
    session = await session_ctx.__aenter__()
    await session.initialize()
    
    tools = await load_mcp_tools(session)
    model = ChatOpenAI(model="gpt-4o-mini")
    
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=system_prompt
    )
    
    return agent, session, session_ctx, stdio_ctx

async def get_agent_response(query):
    agent, session, session_ctx, stdio_ctx = await create_agent_with_tools()
    
    try:
        response = await agent.ainvoke({"messages": [("user", query)]})
        return response["messages"][-1].content
    finally:
        # Clean up
        await session_ctx.__aexit__(None, None, None)
        await stdio_ctx.__aexit__(None, None, None)

async def main():
    agent, session, session_ctx, stdio_ctx = await create_agent_with_tools()
    return agent

if __name__ == "__main__":
    agent = asyncio.run(main())








          