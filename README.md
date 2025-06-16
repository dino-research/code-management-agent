# GitHub Agent - ADK Agent cho GitHub Integration

Đây là một ADK (Agent Development Kit) agent được thiết kế để tương tác với GitHub repositories sử dụng **session-based approach**. Agent này có thể hỏi thông tin GitHub URL và Personal Access Token từ người dùng, sau đó sử dụng **Direct GitHub API** để thực hiện các tác vụ GitHub với hỗ trợ multi-user.

## 🚀 Tính năng

- **Session-based Authentication**: Mỗi user có session riêng biệt với PAT isolation
- **Multi-user Support**: Hỗ trợ nhiều người dùng đồng thời mà không xung đột
- **Direct GitHub API**: Tương tác trực tiếp với GitHub REST API
- **Dynamic Setup**: Thu thập PAT trong cuộc trò chuyện, không cần environment variables
- **Auto Cleanup**: Session tự động cleanup sau 24 giờ
- **Security First**: Token isolation và secure storage trong memory
- **Đa dạng tác vụ**: Hỗ trợ clone repository, xem files, search code, quản lý pull requests, etc.
- **Giao diện tiếng Việt**: Tương tác hoàn toàn bằng tiếng Việt

## 📋 Yêu cầu

### Dependencies
- Python 3.11+
- Google ADK (`google-adk>=1.0.0`)
- requests library cho GitHub API calls

### Không cần cài đặt thêm
- ❌ Không cần github-mcp-server binary
- ❌ Không cần Go programming language
- ❌ Không cần environment variables setup

## 🔧 Cài đặt

### 1. Clone repository này
```bash
git clone <this-repo-url>
cd github-mcp-agent
```

### 2. Cài đặt dependencies
```bash
# Sử dụng setup script (recommended)
chmod +x setup.sh
./setup.sh

# Hoặc manual install
pip install -r requirements.txt
```

## 🎯 Kiến trúc

### Core Components

1. **github_agent/agent.py**: Main ADK agent với session-based approach
2. **github_agent/prompt.py**: System instructions và workflow prompts
3. **github_agent/tools.py**: Session-based tools và validation functions
4. **github_agent/session_manager.py**: Quản lý session và PAT storage
5. **github_agent/github_api_client.py**: Direct GitHub API client

### Flow Diagram

```
User Input → GitHub Agent → Session Manager → GitHub API Client → GitHub API
                             ↓
                          Session Storage (session_id → PAT mapping)
```

## 🔑 Thiết lập GitHub Personal Access Token

### Bước 1: Tạo Token
1. Đăng nhập GitHub.com
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token (classic)

### Bước 2: Cấu hình Permissions
- **repo**: Full control of private repositories ✅
- **read:org**: Read org and team membership ✅ 
- **user:email**: Access user email addresses ✅
- **workflow**: Update GitHub Action workflows (optional)

### Bước 3: Lưu Token
- Copy token: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- Lưu trữ an toàn, không chia sẻ

## 🚀 Sử dụng

### Option 1: ADK Web UI (Recommended)
```bash
# Chạy trong thư mục chứa agent
adk web

# Truy cập http://localhost:8000
# Chọn "github_agent" từ dropdown
```

### Option 2: Programmatic Usage
```python
import asyncio
from github_agent.agent import root_agent
from google.adk.runners import Runner

# Xem example_usage.py để biết chi tiết
```

### Option 3: Command Line
```bash
# Chạy example
python example_usage.py
```

## 💬 Conversation Flow

1. **Agent hỏi GitHub URL**:
   ```
   User: "Tôi muốn làm việc với repository GitHub"
   Agent: "Bạn có thể cung cấp GitHub repository URL không?"
   ```

2. **Agent hỏi Personal Access Token**:
   ```
   User: "https://github.com/microsoft/vscode"
   Agent: "Tôi cần GitHub Personal Access Token để authentication..."
   ```

3. **Agent tạo session**:
   ```
   User: "ghp_your_token_here"
   Agent: "✅ Session đã được tạo thành công! Session ID: abc-123..."
   ```

4. **Agent sử dụng Session-based Tools**:
   ```
   Agent sử dụng session_id để call GitHub API:
   - get_repository_info_session: Lấy thông tin repo
   - get_repository_content_session: Xem files/folders
   - search_code_session: Tìm kiếm code
   - list_pull_requests_session: Xem pull requests
   - clone_repository_session: Clone repository
   - và nhiều tools khác...
   ```

## 🛠️ GitHub Tools Available

Sau khi tạo session thành công, agent có thể sử dụng các tools sau:

### Repository Management
- `get_repository_info_session`: Get repository information
- `get_repository_content_session`: Browse files and folders
- `clone_repository_session`: Clone repository to local

### File Operations  
- `get_file_content_session`: Read file content
- `search_code_session`: Search code across repository

### Pull Request Management
- `list_pull_requests_session`: List repository pull requests
- `get_pull_request_session`: Get specific pull request details

### Session Management
- `list_sessions`: List all active sessions (admin)
- `cleanup_expired_sessions`: Clean up expired sessions

## 🔒 Bảo mật

### Session Security
- ✅ **Session Isolation**: Mỗi user có session riêng biệt
- ✅ **Memory Storage**: Token chỉ lưu trong memory, không write ra disk
- ✅ **Auto Cleanup**: Session tự động xóa sau 24 giờ
- ✅ **Thread Safe**: Session manager thread-safe cho concurrent users
- ✅ **No Environment Pollution**: Không thay đổi environment variables

### Best Practices
- Sử dụng token với expiration date
- Monitor token usage qua GitHub
- Revoke token nếu nghi ngờ compromise
- Không commit token vào version control

## 🧪 Testing

```bash
# Test installation
python -c "from github_agent.agent import root_agent; print('✅ Agent loaded successfully')"

# Test with ADK Web UI
adk web
```

## 🏗️ Phát triển

### Cấu trúc dự án
```
github_agent/
├── agent.py                 # Main ADK agent
├── prompt.py                # System prompts
├── tools.py                 # Session-based tools
├── session_manager.py       # Session management
├── github_api_client.py     # GitHub API client
└── __init__.py             # Package init
```

### Thêm tính năng mới
1. Thêm method vào `GitHubAPIClient` trong `github_api_client.py`
2. Tạo wrapper function trong `tools.py`
3. Thêm tool vào `agent.py`

## 🔄 Migration từ Version 1.x

Nếu bạn đang sử dụng version cũ với github-mcp-server:

1. **Cập nhật code**: Pull latest version
2. **Reinstall**: Chạy `./setup.sh` để cài đặt dependencies mới
3. **Remove old binaries**: Không cần github-mcp-server nữa
4. **Update workflow**: Sử dụng session-based approach

Xem `MIGRATION_GUIDE.md` để biết chi tiết.

## 📊 Performance & Scalability

### Improvements so với Version 1.x
- **🚀 Faster**: Direct API calls, không qua github-mcp-server
- **📈 Scalable**: Hỗ trợ unlimited concurrent users
- **🔒 Secure**: Session isolation và token management
- **🛠️ Maintainable**: Ít dependencies, dễ debug

### Benchmarks
- **Startup time**: ~2 seconds (vs ~10 seconds với github-mcp-server)
- **Memory usage**: ~50MB base (vs ~100MB với external binary)
- **Concurrent users**: Tested với 100+ simultaneous sessions

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Create GitHub issue cho bugs/feature requests
- **Questions**: Discussion tab cho general questions
- **Documentation**: Xem `MIGRATION_GUIDE.md` cho migration help

## 🤖 Agent2Agent (A2A) Protocol Support

GitHub Agent hiện đã tích hợp với **Agent2Agent (A2A) Protocol** của Google, cho phép giao tiếp với other AI agents!

### 🌟 A2A Features

- **Multi-Agent Communication**: Giao tiếp với other agents thông qua standardized protocol
- **Task Delegation**: Delegate GitHub tasks cho specialized agents
- **Collaborative Workflows**: Xây dựng workflows với multiple agents
- **Agent Discovery**: Tự động discover và connect với other A2A agents

### 🚀 Quick Start A2A

```bash
# 1. Start GitHub Agent như A2A Server
python -m github_agent --host localhost --port 10003

# 2. Test A2A integration
python test_a2a_client.py

# 3. Giao tiếp với GitHub Agent từ other agents
from a2a.client import A2AClient
client = A2AClient("http://localhost:10003")
response = client.send_message("Clone repository https://github.com/microsoft/vscode")
```

### 📋 A2A Skills Exported

- **GitHub Repository Management**: Clone, browse, analyze repositories
- **Pull Request Management**: List, review, analyze PRs
- **Code Search and Analysis**: Search patterns, find functions
- **Session Management**: Secure token handling, multi-user support

### 🔗 Multi-Agent Workflows

```python
# Example: GitHub → Analysis → Report pipeline
github_agent = A2AClient("http://localhost:10003")    # GitHub ops
analyzer_agent = A2AClient("http://localhost:10004")  # Code analysis  
reporter_agent = A2AClient("http://localhost:10005")  # Reports

# Chain agents together for complex workflows
async def code_analysis_pipeline(repo_url):
    github_data = await github_agent.process(repo_url)
    analysis = await analyzer_agent.process(github_data)
    report = await reporter_agent.generate(analysis)
    return report
```

Xem [A2A Integration Guide](./A2A_INTEGRATION_GUIDE.md) để biết chi tiết!

## 🔮 Roadmap

- [x] **Agent2Agent (A2A) Protocol**: Multi-agent communication support ✅
- [ ] **A2A Streaming**: Real-time response streaming cho long operations
- [ ] **A2A Discovery**: Enhanced agent discovery với filtering
- [ ] **Session Persistence**: Lưu session vào database
- [ ] **Rate Limiting**: Implement rate limiting per session
- [ ] **Audit Logging**: Log activities cho security
- [ ] **GitHub Apps Support**: Hỗ trợ GitHub Apps authentication
- [ ] **Webhook Integration**: Real-time repository events
- [ ] **Advanced Search**: Semantic code search capabilities