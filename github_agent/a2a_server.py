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
        """Khởi tạo GitHub Agent A2A Wrapper"""
        self.agent_capabilities = AgentCapabilities(
            streaming=True,
            delegation=True,  # Cho phép delegate tasks to other agents
            collaboration=True  # Cho phép collaborate với other agents
        )
        
        # Define skills mà GitHub Agent có thể thực hiện
        self.agent_skills = [
            AgentSkill(
                id='github_repository_management',
                name='GitHub Repository Management',
                description='Quản lý GitHub repositories: xem thông tin, clone, browse files, search code',
                tags=['github', 'repository', 'version-control', 'code-management'],
                examples=[
                    'Clone repository GitHub về local',
                    'Xem thông tin repository và branches',
                    'Browse files và folders trong repository',
                    'Tìm kiếm code trong repository'
                ]
            ),
            AgentSkill(
                id='pull_request_management',
                name='GitHub Pull Request Management', 
                description='Quản lý pull requests: liệt kê, xem chi tiết, phân tích diff',
                tags=['github', 'pull-request', 'code-review', 'collaboration'],
                examples=[
                    'Liệt kê tất cả pull requests',
                    'Xem chi tiết một pull request cụ thể',
                    'Phân tích diff của pull request',
                    'Review changes trong pull request'
                ]
            ),
            AgentSkill(
                id='code_search_analysis',
                name='Code Search and Analysis',
                description='Tìm kiếm và phân tích code trong GitHub repositories',
                tags=['search', 'code-analysis', 'patterns', 'functions'],
                examples=[
                    'Tìm kiếm functions hoặc classes specific',
                    'Tìm patterns trong codebase',
                    'Phân tích code structure',
                    'Search for specific imports or dependencies'
                ]
            ),
            AgentSkill(
                id='session_management',
                name='GitHub Session Management',
                description='Quản lý sessions và authentication với GitHub API',
                tags=['authentication', 'session', 'security', 'github-api'],
                examples=[
                    'Tạo session mới với GitHub repository',
                    'Validate GitHub URLs và tokens',
                    'Quản lý multiple concurrent sessions',
                    'Handle authentication errors'
                ]
            )
        ]
    
    def create_agent_card(self, host: str = 'localhost', port: int = 10003) -> AgentCard:
        """
        Tạo Agent Card cho GitHub Agent A2A Server
        
        Args:
            host: Host address
            port: Port number
            
        Returns:
            AgentCard instance
        """
        return AgentCard(
            name='GitHub Code Management Agent',
            description='AI Agent chuyên biệt để quản lý GitHub repositories, pull requests, và code analysis sử dụng GitHub API',
            url=f'http://{host}:{port}/',
            version='2.1.0',  # Version với A2A support
            defaultInputModes=self.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=self.SUPPORTED_CONTENT_TYPES,
            capabilities=self.agent_capabilities,
            skills=self.agent_skills,
            # Metadata cho A2A discovery
            metadata={
                'framework': 'Google ADK',
                'specialization': 'GitHub Integration',
                'languages': ['Vietnamese', 'English'],
                'github_api_version': 'v3',
                'supported_repositories': 'public and private',
                'collaboration_features': [
                    'multi-agent task delegation',
                    'code analysis sharing',
                    'repository information exchange'
                ]
            }
        )
    
    def create_a2a_server(self, host: str = 'localhost', port: int = 10003) -> A2AStarletteApplication:
        """
        Tạo A2A Starlette Application server
        
        Args:
            host: Host address
            port: Port number
            
        Returns:
            A2AStarletteApplication instance
        """
        agent_card = self.create_agent_card(host, port)
        
        # Create request handler với GitHub Agent Executor
        request_handler = DefaultRequestHandler(
            agent_executor=GitHubAgentExecutor(),
            task_store=InMemoryTaskStore(),
        )
        
        # Create A2A Starlette Application
        server = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=request_handler
        )
        
        return server
    
    def get_processing_message(self) -> str:
        """
        Message hiển thị khi đang process request
        
        Returns:
            Processing message string
        """
        return 'Đang xử lý yêu cầu GitHub... 🔄'


def create_github_a2a_server(host: str = 'localhost', port: int = 10003) -> A2AStarletteApplication:
    """
    Factory function để tạo GitHub Agent A2A Server
    
    Args:
        host: Host address  
        port: Port number
        
    Returns:
        A2AStarletteApplication ready to run
    """
    wrapper = GitHubAgentA2AWrapper()
    return wrapper.create_a2a_server(host, port)


if __name__ == '__main__':
    # Development server startup
    import uvicorn
    
    logger.info("🚀 Khởi động GitHub Agent A2A Server...")
    
    # Create server instance
    server = create_github_a2a_server()
    app = server.build()
    
    # Run server
    uvicorn.run(app, host='localhost', port=10003, log_level='info') 