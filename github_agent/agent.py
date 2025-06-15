"""
GitHub Agent - ADK agent để làm việc với GitHub thông qua github-mcp-server và MCP tools
"""
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from google.adk.tools import FunctionTool
from mcp.client.stdio import StdioServerParameters
from . import prompt
from pathlib import Path
from .tools import (
    validate_github_url,
    validate_github_token,
    setup_github_environment,
    clone_repository,
    get_repository_info,
    show_github_setup_guide,
    initialize_github_mcp_connection
)
from dotenv import load_dotenv
load_dotenv()

# Sử dụng Gemini 2.0 Flash cho hiệu suất tốt nhất
MODEL = "gemini-2.0-flash-exp"

# Tạo tool để initialize MCP connection
initialize_mcp_tool = FunctionTool(initialize_github_mcp_connection)

# Tạo MCPToolset để kết nối với github-mcp-server
# Sẽ được khởi tạo với dummy environment ban đầu
github_mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=str((Path(__file__).parent.parent / "github-mcp-server" / "github-mcp-server").resolve()),
            args=["stdio"],  # Use stdio subcommand for MCP protocol
            env={
                # Set dummy token ban đầu, sẽ được cập nhật bởi initialize_mcp_tool
                "GITHUB_PERSONAL_ACCESS_TOKEN": "dummy_token_will_be_replaced"
            }
        )
    )
)

# Tạo GitHub Agent chính
github_agent = LlmAgent(
    model=MODEL,
    name="github_agent",
    description="AI agent chuyên biệt để làm việc với GitHub repositories thông qua github-mcp-server",
    instruction=prompt.GITHUB_AGENT_PROMPT,
    tools=[
        # Custom tools để validate và setup
        FunctionTool(validate_github_url),
        FunctionTool(validate_github_token),
        FunctionTool(setup_github_environment),
        initialize_mcp_tool,  # Tool để setup MCP connection
        FunctionTool(clone_repository),
        FunctionTool(get_repository_info),
        FunctionTool(show_github_setup_guide),
        # MCP toolset từ github-mcp-server
        github_mcp_toolset,
    ],
    # Store output cho debugging
    output_key="github_agent_result"
)

# ADK convention: export root_agent để có thể discover
root_agent = github_agent 