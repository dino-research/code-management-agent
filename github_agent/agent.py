"""
GitHub Agent - ADK agent để làm việc với GitHub sử dụng session-based approach
Thay thế github-mcp-server để hỗ trợ multi-user
"""
import os
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from . import prompt
from .tools import (
    validate_github_url,
    validate_github_token,
    show_github_setup_guide,
    create_github_session,
    get_repository_info_session,
    clone_repository_session,
    get_repository_content_session,
    get_file_content_session,
    list_pull_requests_session,
    get_pull_request_session,
    get_pull_request_diff_session,
    search_code_session,
    list_sessions,
    cleanup_expired_sessions
)
from dotenv import load_dotenv
load_dotenv()

# Sử dụng Gemini 2.0 Flash cho hiệu suất tốt nhất
MODEL = "gemini-2.0-flash-exp"

# Tạo GitHub Agent với session-based approach
github_agent = LlmAgent(
    model=MODEL,
    name="github_agent",
    description="AI agent chuyên biệt để làm việc với GitHub repositories sử dụng session-based approach",
    instruction=prompt.GITHUB_AGENT_PROMPT_NEW,
    tools=[
        # Validation tools
        FunctionTool(validate_github_url),
        FunctionTool(validate_github_token),
        FunctionTool(show_github_setup_guide),
        
        # Session-based tools
        FunctionTool(create_github_session),
        FunctionTool(get_repository_info_session),
        FunctionTool(clone_repository_session),
        FunctionTool(get_repository_content_session),
        FunctionTool(get_file_content_session),
        FunctionTool(list_pull_requests_session),
        FunctionTool(get_pull_request_session),
        FunctionTool(get_pull_request_diff_session),
        FunctionTool(search_code_session),
        
        # Session management tools
        FunctionTool(list_sessions),
        FunctionTool(cleanup_expired_sessions),
    ],
    # Store output cho debugging
    output_key="github_agent_result"
)

# ADK convention: export root_agent để có thể discover
root_agent = github_agent 