# GitHub Agent A2A Integration Guide

Hướng dẫn tích hợp GitHub Agent với Agent2Agent (A2A) Protocol để giao tiếp với other agents.

## 🌟 Tổng quan

GitHub Agent đã được tích hợp với **Agent2Agent (A2A) Protocol** của Google, cho phép:

- **Multi-Agent Communication**: Giao tiếp với other AI agents thông qua standardized protocol
- **Task Delegation**: Delegate GitHub tasks cho specialized agents
- **Collaborative Workflows**: Xây dựng workflows với multiple agents
- **Interoperability**: Hoạt động với bất kỳ A2A-compatible agent nào

## 🏗️ Kiến trúc A2A Integration

```
┌─────────────────┐    A2A Protocol    ┌─────────────────┐
│   Other Agent   │ ←──────────────→   │  GitHub Agent   │
│                 │                    │                 │ 
│ - Analysis      │    HTTP/JSON       │ - Repository    │
│ - Reporting     │    Messages        │ - Pull Requests │
│ - Planning      │                    │ - Code Search   │
└─────────────────┘                    └─────────────────┘
        ↓                                       ↓
┌─────────────────┐                    ┌─────────────────┐
│  A2A Client     │                    │  A2A Server     │
│                 │                    │                 │
│ - Send Tasks    │                    │ - Agent Card    │
│ - Receive Data  │                    │ - Skills Export │
│ - Workflow Mgmt │                    │ - Task Handling │
└─────────────────┘                    └─────────────────┘
```

## 🚀 Cài đặt và Setup

### 1. Cài đặt Dependencies

```bash
# Cài đặt A2A SDK
pip install a2a-sdk>=0.2.7

# Hoặc cài đặt tất cả dependencies
pip install -r requirements.txt
```

### 2. Kiểm tra A2A Dependencies

Requirements mới bao gồm:
```
google-adk>=1.0.0
pydantic>=2.0.0
requests>=2.31.0
a2a-sdk>=0.2.7          # 🆕 A2A Protocol support
uvicorn>=0.27.0         # 🆕 A2A Server
starlette>=0.40.0       # 🆕 A2A Web framework
click>=8.1.8            # 🆕 CLI support
python-dotenv>=1.1.0    # 🆕 Environment variables
```

## 🖥️ Chạy GitHub Agent như A2A Server

### Option 1: Command Line Interface

```bash
# Chạy GitHub Agent A2A Server
python -m github_agent --host localhost --port 10003

# Chạy với debug mode
python -m github_agent --host 0.0.0.0 --port 10003 --debug

# Chạy trên production
python -m github_agent --host 0.0.0.0 --port 80
```

### Option 2: Programmatic

```python
from github_agent.a2a_server import create_github_a2a_server
import uvicorn

# Tạo server
server = create_github_a2a_server(host='localhost', port=10003)
app = server.build()

# Run server
uvicorn.run(app, host='localhost', port=10003)
```

## 🔗 Agent Card và Skills

GitHub Agent expose following skills qua A2A:

### **🔧 GitHub Repository Management**
- Clone repositories về local
- Browse files và folders
- Xem repository information
- Access branch và commit history

### **🔀 Pull Request Management** 
- List pull requests
- View pull request details
- Analyze pull request diffs
- Review code changes

### **🔍 Code Search and Analysis**
- Search code patterns
- Find functions và classes
- Analyze code structure
- Search dependencies

### **🔑 Session Management**
- Create secure GitHub sessions
- Manage authentication tokens
- Handle multiple concurrent users
- Auto cleanup expired sessions

## 🤖 Giao tiếp với GitHub Agent

### A2A Client Example

```python
from a2a.client import A2AClient
from a2a.types import Message, TextContent, MessageRole

# Tạo A2A client
client = A2AClient("http://localhost:10003")

# Gửi message
message = Message(
    content=TextContent(text="Hãy clone repository https://github.com/microsoft/vscode"),
    role=MessageRole.USER
)

response = client.send_message(message)
print(response.content.text)
```

### Async A2A Communication

```python
import asyncio
from a2a.client import A2AClient

async def github_workflow():
    client = A2AClient("http://localhost:10003")
    
    # Async message
    message = Message(
        content=TextContent(text="Tôi muốn phân tích repository này"),
        role=MessageRole.USER
    )
    
    response = await client.send_message_async(message)
    return response

# Run workflow
result = asyncio.run(github_workflow())
```

## 🌐 Multi-Agent Workflows

### Example: Code Analysis Pipeline

```python
from a2a.client import A2AClient

# Setup multiple agents
github_agent = A2AClient("http://localhost:10003")    # GitHub operations
analyzer_agent = A2AClient("http://localhost:10004")  # Code analysis  
reporter_agent = A2AClient("http://localhost:10005")  # Report generation

async def code_analysis_pipeline(repo_url):
    # Step 1: GitHub Agent gets repository data
    github_result = await github_agent.send_message_async(
        Message(
            content=TextContent(text=f"Clone và extract code từ {repo_url}"),
            role=MessageRole.USER
        )
    )
    
    # Step 2: Analyzer Agent processes code
    analysis_result = await analyzer_agent.send_message_async(
        Message(
            content=TextContent(text=f"Analyze code: {github_result.content.text}"),
            role=MessageRole.USER
        )
    )
    
    # Step 3: Reporter Agent generates report
    report = await reporter_agent.send_message_async(
        Message(
            content=TextContent(text=f"Generate report: {analysis_result.content.text}"),
            role=MessageRole.USER
        )
    )
    
    return report

# Execute pipeline
result = asyncio.run(code_analysis_pipeline("https://github.com/facebook/react"))
```

## 🔧 Agent Discovery và Registry

### Đăng ký GitHub Agent với A2A Registry

```python
from a2a.discovery import AgentRegistry, enable_discovery

# Enable automatic discovery
registry_url = "http://localhost:8000"  # A2A Registry server
discovery_client = enable_discovery(github_agent, registry_url=registry_url)

# GitHub Agent sẽ tự động register skills và capabilities
```

### Discover GitHub Agent từ other agents

```python
from a2a.discovery import DiscoveryClient

# Tạo discovery client
client = DiscoveryClient()
client.add_registry("http://localhost:8000")

# Discover all agents
agents = client.discover()

# Find GitHub Agent
github_agents = [agent for agent in agents if "github" in agent.name.lower()]
for agent in github_agents:
    print(f"Found: {agent.name} at {agent.url}")
    print(f"Skills: {[skill.name for skill in agent.skills]}")
```

## 📊 Monitoring và Debugging

### Health Check

```bash
# Check if GitHub Agent A2A Server is running
curl http://localhost:10003/health

# Get Agent Card information
curl http://localhost:10003/agent-card
```

### Debug Mode

```bash
# Run with full debug logging
python -m github_agent --debug

# This enables:
# - Detailed A2A protocol logs
# - GitHub API call tracing  
# - Session management logs
# - Error stack traces
```

### Logs Example

```
🚀 Khởi động GitHub Agent A2A Server...
📍 Server sẽ chạy tại: http://localhost:10003
🔗 A2A endpoint: http://localhost:10003/a2a
✅ GitHub Agent A2A Server đã sẵn sàng!
📋 Skills available:
  - GitHub Repository Management
  - Pull Request Management  
  - Code Search and Analysis
  - Session Management
```

## 🧪 Testing A2A Integration

### Run Test Suite

```bash
# Start GitHub Agent A2A Server
python -m github_agent --port 10003

# Run test client trong terminal khác
python test_a2a_client.py
```

### Test Output Example

```
🔥 GitHub Agent A2A Integration Test Suite
============================================================
✅ GitHub Agent A2A Server is running!

1️⃣ Running Synchronous Tests...
🚀 Testing GitHub Agent A2A Integration (Sync)...
📤 Sending simple message...
📥 Response:
✅ Xin chào! Tôi là GitHub Agent và tôi sẽ giúp bạn làm việc với GitHub repository...

2️⃣ Running Asynchronous Tests...
🚀 Testing GitHub Agent A2A Integration...
============================================================
📋 Test Case 1: Agent Info Request
💬 Message: Xin chào! Bạn có thể giới thiệu về GitHub Agent không?
📤 Sending to GitHub Agent via A2A...
📥 Response received:
✅ [Detailed GitHub Agent introduction...]

🎉 A2A Integration Test Complete!
```

## 🔄 Integration Patterns

### 1. **Task Delegation Pattern**

```python
# GitHub Agent delegates analysis to specialized agent
async def delegate_analysis(repo_data):
    analysis_agent = A2AClient("http://localhost:10004")
    
    result = await analysis_agent.send_message_async(
        Message(
            content=TextContent(text=f"Analyze this GitHub repo data: {repo_data}"),
            role=MessageRole.USER
        )
    )
    return result
```

### 2. **Data Pipeline Pattern**

```python
# Chain multiple agents for complex workflows
async def github_to_report_pipeline(repo_url):
    # GitHub → Data Extraction
    github_data = await github_agent.get_repo_data(repo_url)
    
    # Data → Analysis
    analysis = await analysis_agent.process(github_data)
    
    # Analysis → Report
    report = await report_agent.generate(analysis)
    
    return report
```

### 3. **Collaborative Pattern**

```python
# Multiple agents work on same task
async def collaborative_code_review(pr_url):
    # GitHub Agent gets PR data
    pr_data = await github_agent.get_pr_data(pr_url)
    
    # Parallel analysis by different specialized agents
    tasks = [
        security_agent.check_security(pr_data),
        performance_agent.check_performance(pr_data), 
        style_agent.check_style(pr_data)
    ]
    
    results = await asyncio.gather(*tasks)
    return combine_review_results(results)
```

## 🔒 Security và Best Practices

### Authentication Handling

- **Session Isolation**: Mỗi A2A conversation có session riêng
- **Token Security**: GitHub tokens được lưu secure trong session
- **Auto Cleanup**: Sessions tự động expire sau 24h
- **No Token Leakage**: Tokens không expose trong A2A messages

### Production Deployment

```bash
# Production deployment with proper security
python -m github_agent \
    --host 0.0.0.0 \
    --port 80 \
    --no-debug
```

### Environment Variables

```bash
# .env file for production
GOOGLE_API_KEY=your_gemini_api_key
GITHUB_A2A_HOST=0.0.0.0
GITHUB_A2A_PORT=80
GITHUB_A2A_DEBUG=false
```

## 🚀 Advanced Usage

### Custom A2A Skills

```python
# Extend GitHub Agent với custom A2A skills
from github_agent.a2a_server import GitHubAgentA2AWrapper

class CustomGitHubA2AWrapper(GitHubAgentA2AWrapper):
    def __init__(self):
        super().__init__()
        # Add custom skills
        self.agent_skills.append(
            AgentSkill(
                id='custom_github_analysis',
                name='Custom GitHub Analysis',
                description='Advanced GitHub repository analysis',
                tags=['github', 'analysis', 'custom'],
                examples=['Perform deep analysis on repository structure']
            )
        )
```

### Load Balancing Multiple GitHub Agents

```python
# Run multiple GitHub Agent instances
agents = [
    A2AClient("http://localhost:10003"),  # Instance 1
    A2AClient("http://localhost:10004"),  # Instance 2  
    A2AClient("http://localhost:10005"),  # Instance 3
]

# Simple round-robin load balancer
class GitHubAgentPool:
    def __init__(self, agents):
        self.agents = agents
        self.current = 0
    
    def get_agent(self):
        agent = self.agents[self.current]
        self.current = (self.current + 1) % len(self.agents)
        return agent

pool = GitHubAgentPool(agents)
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :10003
   
   # Kill process và restart
   kill -9 <PID>
   python -m github_agent --port 10003
   ```

2. **A2A Import Errors**
   ```bash
   # Reinstall A2A SDK
   pip uninstall a2a-sdk
   pip install a2a-sdk>=0.2.7
   ```

3. **GitHub Session Issues**
   ```python
   # Clear expired sessions
   from github_agent.session_manager import session_manager
   session_manager.cleanup_expired_sessions(max_age_hours=1)
   ```

### Debug Commands

```bash
# Test A2A endpoint directly
curl -X POST http://localhost:10003/a2a \
  -H "Content-Type: application/json" \
  -d '{"message": {"content": {"text": "Hello"}, "role": "user"}}'

# Check agent card
curl http://localhost:10003/agent-card | jq .

# Health check
curl http://localhost:10003/health
```

## 🎯 Roadmap

### Planned Features

- [ ] **Streaming Support**: Real-time response streaming for long operations
- [ ] **Enhanced Discovery**: Advanced agent discovery với filtering
- [ ] **Workflow Templates**: Pre-built A2A workflow templates
- [ ] **Performance Monitoring**: Metrics cho A2A operations
- [ ] **Authentication Integration**: OAuth2 support cho A2A
- [ ] **UI Dashboard**: Web dashboard để monitor A2A agents

### Community Contributions

Contributions welcome! Areas:
- Additional A2A skills
- Integration examples
- Performance optimizations
- Documentation improvements

## 📚 Tài liệu tham khảo

- [Google A2A Protocol Specification](https://google-a2a.github.io/A2A/latest/)
- [A2A Python SDK Documentation](https://github.com/google-a2a/a2a-python)
- [A2A Samples Repository](https://github.com/google-a2a/a2a-samples)
- [GitHub Agent Documentation](./README.md)

---

**✨ GitHub Agent giờ đây đã sẵn sàng cho multi-agent collaboration thông qua A2A Protocol!**

Để bắt đầu:
1. Start GitHub Agent A2A Server: `python -m github_agent`
2. Test integration: `python test_a2a_client.py`  
3. Build your multi-agent workflows! 🚀 