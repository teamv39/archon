from fastmcp import FastMCP

mcp = FastMCP("Archon Context Server")

@mcp.tool()
async def ping():
    return "pong"

if __name__ == "__main__":
    mcp.run()