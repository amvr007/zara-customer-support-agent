from query_engine import support_engine, recommendation_engine
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("zarasrvr")

@mcp.tool()
def support_client(query:str) -> str:
    """Search Zara support documentation for policies, shipping, returns, sizing, and customer service information."""
    try:
        response = support_engine.query(query)
        return response.response
    except Exception as e:
        return f"Error searching support knowledge: {str(e)}"
    

@mcp.tool()
def recommendation_client(query:str) -> str:
    """recommend products based on user preferences"""
    try:
        response = recommendation_engine.query(query)
        return response.response
    except Exception as e:
        return f"Error searching recommendation knowledge: {str(e)}"
    

if __name__ == "__main__":
    mcp.run()