import asyncio
import os 
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
    env=os.environ.copy(),
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write)  as session:
            await session.initialize()

            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

        
def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()