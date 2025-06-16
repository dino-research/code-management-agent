# GitHub Agent - A2A Compatible Multi-Agent System

🤖 **GitHub Agent** là một AI agent chuyên biệt được thiết kế để tương tác với GitHub repositories và **hỗ trợ Agent2Agent (A2A) Protocol** để giao tiếp với other agents trong hệ thống multi-agent.

## 🌟 Tổng quan

GitHub Agent được xây dựng trên Google ADK và tích hợp với **Agent2Agent (A2A) Protocol**, cho phép:

- **Multi-Agent Communication**: Giao tiếp với other AI agents thông qua standardized protocol
- **GitHub Repository Management**: Quản lý và tương tác với GitHub repositories
- **Session-based Security**: Mỗi agent/user có session riêng biệt và isolated
- **Task Delegation**: Delegate GitHub tasks cho specialized agents
- **Agent Discovery**: Tự động discover và connect với other A2A agents

## 🚀 Tính năng chính

### 🔗 A2A Protocol Support
- ✅ **HTTP/JSON Messaging**: Standardized communication với other agents
- ✅ **Agent Discovery**: Tự động discover agent capabilities
- ✅ **Task Execution**: Nhận và thực thi tasks từ other agents
- ✅ **Event-driven Architecture**: Real-time updates và notifications
- ✅ **Error Handling**: Robust error handling và status reporting

### 🐙 GitHub Integration
- ✅ **Repository Management**: Clone, browse, analyze repositories
- ✅ **Pull Request Management**: View, analyze PR diffs và changes
- ✅ **Code Search**: Tìm kiếm code across repositories
- ✅ **Session-based Authentication**: Secure PAT management per session
- ✅ **Multi-user Support**: Isolated sessions cho multiple users/agents

### 🛡️ Security & Reliability
- ✅ **Session Isolation**: Mỗi agent interaction có session riêng
- ✅ **Token Security**: PAT được stored securely in memory
- ✅ **Auto Cleanup**: Sessions tự động cleanup sau 24 giờ
- ✅ **Thread Safe**: Concurrent access support

## 📋 Yêu cầu hệ thống

- **Python 3.11+**
- **Google ADK** (`google-adk>=1.0.0`)
- **A2A SDK** (`a2a-sdk>=0.2.7`)
- **Google Cloud CLI** (for authentication)

## 🔧 Cài đặt nhanh

### 1. Clone repository
```bash
git clone https://github.com/dino-research/code-management-agent.git
cd code-management-agent
```

### 2. Chạy setup script
```bash
chmod +x setup.sh
./setup.sh
```

Setup script sẽ:
- ✅ Kiểm tra Python 3.11+
- ✅ Tạo virtual environment
- ✅ Cài đặt tất cả dependencies (bao gồm A2A SDK)
- ✅ Kiểm tra Google Cloud authentication

## 🎯 Modes hoạt động

### Mode 1: A2A Server (Multi-Agent Systems) 🌟

**Khuyến nghị cho multi-agent systems**

```bash
source venv/bin/activate
python -m github_agent --host localhost --port 10003
```

GitHub Agent sẽ chạy như một A2A server, sẵn sàng nhận requests từ other agents:

```
╔══════════════════════════════════════════════════════════════╗
║                    🤖 GitHub Agent A2A Server                ║
║                                                              ║
║  🌐 Host: localhost          🔌 Port: 10003                  ║
║  🔧 Debug: Disabled          📊 A2A Protocol: Ready          ║
║                                                              ║
║  🚀 Server starting...                                       ║
╚══════════════════════════════════════════════════════════════╝
```

### Mode 2: Traditional ADK Web

```bash
source venv/bin/activate
adk web
```
Truy cập http://localhost:8000 và chọn "github_agent"

## 🤝 A2A Agent Communication

### Agent Capabilities

GitHub Agent expose các capabilities sau qua A2A Protocol:

```json
{
  "name": "GitHub Agent",
  "description": "AI agent chuyên biệt để làm việc với GitHub repositories",
  "capabilities": {
    "skills": [
      {
        "name": "github_repository_management",
        "description": "Quản lý và tương tác với GitHub repositories"
      },
      {
        "name": "code_analysis", 
        "description": "Phân tích code và repository structure"
      },
      {
        "name": "pull_request_management",
        "description": "Xem và quản lý pull requests"
      },
      {
        "name": "repository_cloning",
        "description": "Clone repositories về local"
      },
      {
        "name": "code_search",
        "description": "Tìm kiếm code trong repositories"
      }
    ],
    "supported_content_types": ["text", "text/plain", "application/json"]
  }
}
```

### Communication Examples

**Từ other agent đến GitHub Agent:**

```python
from a2a.client import A2AClient

# Connect to GitHub Agent
client = A2AClient("http://localhost:10003")

# Request GitHub repository analysis
response = await client.send_message(
    "Phân tích repository https://github.com/microsoft/vscode với PAT: ghp_your_token"
)

# GitHub Agent sẽ:
# 1. Validate GitHub URL và PAT
# 2. Tạo session
# 3. Thực hiện analysis
# 4. Trả về kết quả qua A2A Protocol
```

**HTTP Request Example:**

```bash
curl -X POST http://localhost:10003/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Clone repository https://github.com/owner/repo với PAT: ghp_token_here"
  }'
```

## 🔑 GitHub Authentication

### Personal Access Token Setup

1. **Tạo GitHub PAT:**
   - GitHub.com → Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Permissions: `repo`, `read:org`, `user:email`

2. **Sử dụng với GitHub Agent:**
   ```
   Tôi muốn làm việc với repository https://github.com/owner/repo
   PAT: ghp_your_token_here
   ```

GitHub Agent sẽ tự động:
- ✅ Validate URL và token format
- ✅ Test connection với GitHub API
- ✅ Tạo isolated session
- ✅ Thực hiện GitHub operations

## 🛠️ GitHub Operations

Sau khi authentication thành công, GitHub Agent có thể:

### Repository Management
- 📖 **Repository Info**: Lấy thông tin repository (stars, language, description)
- 📁 **Browse Content**: Xem files và folders structure
- 📥 **Clone Repository**: Clone về local với auto temp folder management

### Code Analysis
- 🔍 **Code Search**: Tìm kiếm code patterns across repository
- 📄 **File Content**: Đọc và analyze file content
- 🌳 **Directory Exploration**: Navigate repository structure

### Pull Request Management
- 📋 **List PRs**: Xem danh sách pull requests (open/closed/all)
- 🔍 **PR Details**: Chi tiết pull request với metadata
- 📊 **PR Diff**: Xem diff changes trong markdown format

### Session Management
- 👥 **Multi-user**: Isolated sessions cho multiple agents/users
- 🧹 **Auto Cleanup**: Tự động cleanup expired sessions
- 📊 **Session Monitoring**: Track active sessions và usage

## 🏗️ Multi-Agent Architecture

### Typical A2A Workflow

```
┌─────────────────┐    A2A Protocol    ┌─────────────────┐
│   Analysis      │ ←──────────────→   │  GitHub Agent   │
│   Agent         │                    │                 │ 
│                 │    HTTP/JSON       │ - Repository    │
│ - Code Review   │    Messages        │ - Pull Requests │
│ - Security Scan │                    │ - Code Search   │
│ - Documentation │                    │ - File Content  │
└─────────────────┘                    └─────────────────┘
         ↑                                       ↑
         │              A2A Protocol             │
         ↓                                       ↓
┌─────────────────┐                    ┌─────────────────┐
│   Reporting     │                    │   Task Manager  │
│   Agent         │                    │   Agent         │
│                 │                    │                 │
│ - Generate      │                    │ - Orchestration │
│   Reports       │                    │ - Task Queue    │
│ - Send Alerts   │                    │ - Monitoring    │
└─────────────────┘                    └─────────────────┘
```

### Use Cases

1. **Code Review Automation:**
   - Task Manager → GitHub Agent: "Get PR #123 diff"
   - GitHub Agent → Analysis Agent: "Analyze this code diff"
   - Analysis Agent → Reporting Agent: "Generate review report"

2. **Repository Health Check:**
   - Monitor Agent → GitHub Agent: "Check repo health"
   - GitHub Agent → Security Agent: "Scan for vulnerabilities"
   - Security Agent → Alert Agent: "Send notifications"

3. **Multi-repo Analysis:**
   - Orchestrator → GitHub Agent: "Clone multiple repos"
   - GitHub Agent → Data Agent: "Process repository data"
   - Data Agent → Visualization Agent: "Create dashboards"

## 🧪 Testing A2A Integration

### Start GitHub Agent A2A Server
```bash
# Terminal 1: Start GitHub Agent
python -m github_agent --host localhost --port 10003 --debug
```

### Test from other agents
```python
# Terminal 2: Test client
import asyncio
from a2a.client import A2AClient

async def test_github_agent():
    client = A2AClient("http://localhost:10003")
    
    # Test GitHub repository access
    response = await client.send_message(
        "GitHub URL: https://github.com/microsoft/vscode, PAT: ghp_your_token"
    )
    
    print("GitHub Agent Response:", response)

asyncio.run(test_github_agent())
```

### HTTP Testing
```bash
# Simple ping test
curl http://localhost:10003/health

# Agent capabilities
curl http://localhost:10003/agent-card

# Send task
curl -X POST http://localhost:10003/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Xin chào GitHub Agent!"}'
```

## 🔧 Configuration

### Environment Variables
```bash
# Google Cloud (for ADK)
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=your-location

# A2A Server (optional)
export A2A_HOST=localhost
export A2A_PORT=10003
export A2A_DEBUG=true
```

### Server Options
```bash
# Basic usage
python -m github_agent

# Custom host/port
python -m github_agent --host 0.0.0.0 --port 8080

# Debug mode
python -m github_agent --debug
```

## 📊 Monitoring & Debugging

### Logs & Status

A2A Server cung cấp detailed logs:
- 📡 HTTP requests/responses
- 🔄 Task execution status
- ❌ Error handling và recovery
- 📈 Performance metrics

### Health Checks

```bash
# Server health
curl http://localhost:10003/health

# Agent status
curl http://localhost:10003/status

# Active sessions
curl http://localhost:10003/sessions
```

## 🚀 Production Deployment

### Docker Support (Coming Soon)
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 10003
CMD ["python", "-m", "github_agent", "--host", "0.0.0.0", "--port", "10003"]
```

### Scaling Considerations
- **Horizontal Scaling**: Multiple GitHub Agent instances với load balancer
- **Session Storage**: Redis/Database cho persistent sessions
- **Rate Limiting**: GitHub API rate limit management
- **Security**: API authentication và authorization

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/a2a-enhancement`
3. Commit changes: `git commit -m 'Add A2A feature'`
4. Push branch: `git push origin feature/a2a-enhancement`
5. Create Pull Request

## 📚 Resources

- 📖 [Agent2Agent Protocol Documentation](https://google-a2a.github.io/A2A/latest/)
- 🔧 [Google ADK Documentation](https://developers.google.com/adk)
- 🐙 [GitHub API Documentation](https://docs.github.com/rest)
- 🧪 [A2A Samples Repository](https://github.com/google-a2a/a2a-samples)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**🎯 GitHub Agent - Connecting AI agents với GitHub ecosystem through A2A Protocol!** 🤖🔗🐙