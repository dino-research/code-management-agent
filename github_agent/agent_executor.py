"""
Agent Executor để wrap GitHub Agent cho A2A Protocol
Chuyển đổi GitHub Agent của ADK thành A2A-compatible executor
"""
import json
import asyncio
from typing import Dict, Any, Optional

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    DataPart,
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_parts_message,
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError
from .agent import github_agent
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.genai import types


class GitHubAgentExecutor(AgentExecutor):
    """
    Agent Executor để chuyển đổi GitHub Agent ADK thành A2A-compatible
    """
    
    def __init__(self):
        """
        Khởi tạo GitHub Agent Executor
        """
        self.github_agent = github_agent
        self._user_id = 'a2a_user'  # Default user ID cho A2A
        
        # Tạo runner cho ADK agent
        self._runner = Runner(
            app_name=self.github_agent.name,
            agent=self.github_agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """
        Thực thi GitHub Agent cho A2A request
        
        Args:
            context: Request context từ A2A
            event_queue: Queue để gửi events
        """
        try:
            # Lấy user input từ A2A request
            user_input = context.get_user_input()
            task = context.current_task
            
            # Tạo task mới nếu chưa có
            if not task:
                task = new_task(context.message)
                await event_queue.enqueue_event(task)
            
            # Tạo task updater
            updater = TaskUpdater(event_queue, task.id, task.contextId)
            
            # Thông báo đang xử lý
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(
                    "🔄 Đang xử lý yêu cầu GitHub...",
                    task.contextId,
                    task.id
                ),
            )
            
            # Tạo ADK session
            session = await self._runner.session_service.get_session(
                app_name=self.github_agent.name,
                user_id=self._user_id,
                session_id=task.contextId,
            )
            
            if session is None:
                session = await self._runner.session_service.create_session(
                    app_name=self.github_agent.name,
                    user_id=self._user_id,
                    state={},
                    session_id=task.contextId,
                )
            
            # Tạo ADK Content
            content = types.Content(
                role='user', 
                parts=[types.Part.from_text(text=user_input)]
            )
            
            # Thực thi GitHub Agent
            final_response = None
            artifacts = []
            
            async for event in self._runner.run_async(
                user_id=self._user_id, 
                session_id=session.id, 
                new_message=content
            ):
                if event.is_final_response():
                    # Xử lý response cuối cùng
                    if (event.content and 
                        event.content.parts and 
                        event.content.parts[0].text):
                        
                        response_text = '\n'.join(
                            [p.text for p in event.content.parts if p.text]
                        )
                        final_response = response_text
                        
                        # Tạo artifact từ response
                        artifacts.append(
                            Part(root=TextPart(text=response_text))
                        )
                        
                    elif (event.content and 
                          event.content.parts and 
                          any([p.function_response for p in event.content.parts])):
                        
                        # Xử lý function response
                        func_response = next(
                            p.function_response.model_dump()
                            for p in event.content.parts
                            if p.function_response
                        )
                        
                        # Chuyển đổi function response thành text
                        response_text = json.dumps(func_response, ensure_ascii=False, indent=2)
                        final_response = response_text
                        
                        artifacts.append(
                            Part(root=TextPart(text=response_text))
                        )
                        
                else:
                    # Cập nhật progress cho intermediate events
                    await updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            "🔄 Đang xử lý yêu cầu GitHub...",
                            task.contextId,
                            task.id
                        ),
                    )
            
            # Hoàn thành task với artifacts
            if artifacts:
                await updater.add_artifact(artifacts, name='github_response')
                await updater.complete()
            else:
                # Fallback nếu không có artifacts
                await updater.update_status(
                    TaskState.completed,
                    new_agent_text_message(
                        final_response or "✅ Hoàn thành xử lý GitHub",
                        task.contextId,
                        task.id
                    ),
                    final=True,
                )
                
        except Exception as e:
            # Xử lý lỗi
            error_message = f"❌ Lỗi khi xử lý GitHub: {str(e)}"
            print(f"GitHubAgentExecutor error: {e}")  # Debug log
            
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(
                    error_message,
                    task.contextId,
                    task.id
                ),
                final=True,
            )

    async def cancel(
        self, 
        request: RequestContext, 
        event_queue: EventQueue
    ) -> Task | None:
        """
        Hủy execution (không được support)
        
        Args:
            request: Request context
            event_queue: Event queue
            
        Returns:
            None (raises UnsupportedOperationError)
        """
        raise ServerError(error=UnsupportedOperationError())

    def get_processing_message(self) -> str:
        """
        Message hiển thị khi đang process
        
        Returns:
            Processing message string
        """
        return "🔄 Đang xử lý yêu cầu GitHub..."


# Factory function để tạo GitHubAgentExecutor
def create_github_agent_executor() -> GitHubAgentExecutor:
    """
    Factory function để tạo GitHub Agent Executor
    
    Returns:
        GitHubAgentExecutor instance
    """
    return GitHubAgentExecutor() 