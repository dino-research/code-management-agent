"""
A2A Server wrapper cho GitHub Agent
Tích hợp GitHub Agent với Agent2Agent Protocol để cho phép giao tiếp với other agents
"""
import logging
import os
from typing import AsyncIterable, Dict, Any, Optional

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from .agent_executor import GitHubAgentExecutor
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitHubAgentA2AWrapper:
    """
    Wrapper class để tích hợp GitHub Agent với A2A Protocol
    """
    
    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain', 'application/json']
    
    def __init__(self):
        """
        Khởi tạo GitHub Agent A2A Wrapper
        """
        self.agent_executor = GitHubAgentExecutor()
        
    def get_agent_card(self) -> AgentCard:
        """
        Tạo Agent Card cho GitHub Agent
        
        Returns:
            AgentCard với thông tin về GitHub Agent
        """
        return AgentCard(
            name="GitHub Agent",
            description="AI agent chuyên biệt để làm việc với GitHub repositories sử dụng session-based approach",
            capabilities=AgentCapabilities(
                skills=[
                    AgentSkill(
                        name="github_repository_management",
                        description="Quản lý và tương tác với GitHub repositories"
                    ),
                    AgentSkill(
                        name="code_analysis",
                        description="Phân tích code và repository structure"
                    ),
                    AgentSkill(
                        name="pull_request_management", 
                        description="Xem và quản lý pull requests"
                    ),
                    AgentSkill(
                        name="repository_cloning",
                        description="Clone repositories về local"
                    ),
                    AgentSkill(
                        name="code_search",
                        description="Tìm kiếm code trong repositories"
                    )
                ],
                supported_content_types=self.SUPPORTED_CONTENT_TYPES
            ),
            version="1.0.0"
        )


def create_github_a2a_server(host: str = "localhost", port: int = 10003) -> A2AStarletteApplication:
    """
    Tạo A2A Server cho GitHub Agent
    
    Args:
        host: Host để bind server
        port: Port để bind server
        
    Returns:
        A2AStarletteApplication instance
    """
    # Tạo wrapper
    wrapper = GitHubAgentA2AWrapper()
    
    # Tạo task store
    task_store = InMemoryTaskStore()
    
    # Tạo request handler
    request_handler = DefaultRequestHandler(
        agent_executor=wrapper.agent_executor,
        task_store=task_store
    )
    
    # Tạo A2A application
    app = A2AStarletteApplication(
        agent_card=wrapper.get_agent_card(),
        request_handler=request_handler,
        task_store=task_store
    )
    
    logger.info(f"🚀 GitHub Agent A2A Server created on {host}:{port}")
    return app 