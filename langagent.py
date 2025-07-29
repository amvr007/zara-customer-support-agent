import os
import asyncio
from langchain_openai.chat_models import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langgraph.prebuilt import create_react_agent

with open("system_prompt.md", "r") as file:
    system_prompt =  file.read()

async def get_tools():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            return tools

tools = get_tools()




          