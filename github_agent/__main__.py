import logging
import os

import click
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from github_agent.agent import root_agent
from github_agent.agent_executor import GitHubAgentExecutor

from dotenv import load_dotenv
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService


load_dotenv()

logging.basicConfig()

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 10003

def main(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    
    agent_skills = [
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
        )]
    
    agent_capabilities = AgentCapabilities(
        streaming=True,
        delegation=True,  # Cho phép delegate tasks to other agents
        collaboration=True  # Cho phép collaborate với other agents
    )

    agent_card = AgentCard(
        name='GitHub Code Management Agent',
        description='AI Agent chuyên biệt để quản lý GitHub repositories, pull requests, và code analysis sử dụng GitHub API',
        url=f'http://{host}:{port}/',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=agent_capabilities,
        skills=agent_skills,
    )

    runner = Runner(
        app_name=agent_card.name,
        agent=root_agent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )
    agent_executor = GitHubAgentExecutor(runner, agent_card)

    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor, task_store=InMemoryTaskStore()
    )

    a2a_app = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    uvicorn.run(a2a_app.build(), host=host, port=port)


@click.command()
@click.option('--host', 'host', default=DEFAULT_HOST)
@click.option('--port', 'port', default=DEFAULT_PORT)
def cli(host: str, port: int):
    main(host, port)


if __name__ == '__main__':
    main()
