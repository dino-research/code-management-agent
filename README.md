# GitHub Agent - ADK Agent cho GitHub Integration

Đây là một ADK (Agent Development Kit) agent được thiết kế để tương tác với GitHub repositories thông qua [github-mcp-server](https://github.com/github/github-mcp-server). Agent này có thể hỏi thông tin GitHub URL và Personal Access Token từ người dùng, sau đó sử dụng **MCPToolset** để thực hiện các tác vụ GitHub.

## 🚀 Tính năng

- **Thu thập thông tin an toàn**: Hỏi GitHub URL và Personal Access Token từ người dùng
- **Validation**: Kiểm tra tính hợp lệ của GitHub URL và token format
- **GitHub Integration**: Sử dụng github-mcp-server thông qua **MCPToolset** để tương tác với GitHub API
- **Đa dạng tác vụ**: Hỗ trợ clone repository, xem files, search code, quản lý commits, etc.
- **Giao diện tiếng Việt**: Tương tác hoàn toàn bằng tiếng Việt
- **MCPToolset Integration**: Sử dụng ADK MCPToolset để kết nối với github-mcp-server

## 📋 Yêu cầu

### Dependencies
- Python 3.11+
- Google ADK (`google-adk>=1.0.0`)
- github-mcp-server (cài đặt từ [GitHub repository](https://github.com/github/github-mcp-server))

### Cài đặt github-mcp-server

#### Option 1: Từ Go (Recommended)
```bash
# Cài đặt Go nếu chưa có
go install github.com/github/github-mcp-server/cmd/github-mcp-server@latest

# Verify installation
github-mcp-server --help
```

#### Option 2: Download Binary
1. Truy cập [GitHub Releases](https://github.com/github/github-mcp-server/releases)
2. Download binary phù hợp với OS của bạn
3. Đặt binary vào PATH

#### Option 3: Build từ Source
```bash
git clone https://github.com/github/github-mcp-server.git
cd github-mcp-server
go build -o github-mcp-server ./cmd/github-mcp-server
# Copy binary vào PATH
```

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

### 3. Verify github-mcp-server
```bash
# Kiểm tra github-mcp-server có trong PATH
which github-mcp-server
github-mcp-server --help
```

## 🎯 Kiến trúc

### Core Components

1. **github_agent/agent.py**: Main ADK agent với MCPToolset integration
2. **github_agent/prompt.py**: System instructions và workflow prompts
3. **github_agent/tools.py**: Custom validation và setup tools
4. **MCPToolset**: ADK component để kết nối với github-mcp-server

### Flow Diagram

```
User Input → GitHub Agent → Custom Tools (validation/setup) → MCPToolset → github-mcp-server → GitHub API
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

3. **Agent setup environment**:
   ```
   User: "ghp_your_token_here"
   Agent: "✅ Environment đã được setup! Bây giờ tôi có thể sử dụng GitHub MCP tools..."
   ```

4. **Agent sử dụng GitHub MCP Tools**:
   ```
   Agent sử dụng MCPToolset để call github-mcp-server:
   - get_repository: Lấy thông tin repo
   - get_repository_content: Xem files/folders
   - search_code: Tìm kiếm code
   - list_commits: Xem commit history
   - create_branch: Tạo branch mới
   - và nhiều tools khác...
   ```

## 🛠️ GitHub MCP Tools Available

Sau khi setup thành công, agent có thể sử dụng các tools từ github-mcp-server:

### Repository Management
- `get_repository`: Get repository information
- `get_repository_content`: Browse files and folders
- `search_repositories`: Search for repositories

### File Operations  
- `get_file_contents`: Read file content
- `search_code`: Search code across repository
- `get_directory_contents`: List directory contents

### Branch & Commit Management
- `list_branches`: List all branches
- `create_branch`: Create new branch
- `list_commits`: Get commit history
- `get_commit`: Get specific commit details

### Issue & PR Management (if available)
- `list_issues`: List repository issues
- `create_issue`: Create new issue
- `list_pull_requests`: List pull requests

## 🔒 Bảo mật

### Token Security
- ✅ Environment variable isolation
- ✅ Không hardcode token trong code
- ✅ Token validation
- ✅ Secure storage recommendations

### Best Practices
- Sử dụng token với expiration date
- Monitor token usage qua GitHub
- Revoke token nếu nghi ngờ compromise
- Không commit token vào version control

## 🧪 Testing

```bash
# Test individual tools
python -c "
from github_agent.tools import validate_github_url
print(validate_github_url('https://github.com/microsoft/vscode'))
"

# Run full demo
python example_usage.py

# Test với ADK web
adk web
```

## ⚠️ Troubleshooting

### Common Issues

**1. "github-mcp-server not found" Error**
```bash
# Kiểm tra Go đã cài đặt chưa
go version

# Cài đặt github-mcp-server
go install github.com/github/github-mcp-server/cmd/github-mcp-server@latest

# Verify installation
which github-mcp-server
github-mcp-server --help

# Test chạy stdio mode
github-mcp-server stdio --help
```

**2. "FileNotFoundError" khi start MCPToolset**
```bash
# Đảm bảo Go bin directory trong PATH
echo $PATH | grep -q "$HOME/go/bin" || echo 'export PATH=$HOME/go/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Hoặc add vào shell profile
export PATH=$HOME/go/bin:$PATH
```

**3. "MCPToolset connection failed"**
```bash
# Test github-mcp-server manually trước
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"
github-mcp-server stdio

# Verify environment variables
echo $GITHUB_PERSONAL_ACCESS_TOKEN
```

**4. "Permission denied errors"**
```bash
# Check token permissions tại https://github.com/settings/tokens
# Token cần có đúng scopes: repo, read:org, user:email

# Kiểm tra token format
python3 -c "
token = input('Enter token: ')
if token.startswith('ghp_') and len(token) == 40:
    print('✅ Valid classic token format')
elif token.startswith('github_pat_'):
    print('✅ Valid fine-grained token format')
else:
    print('❌ Invalid token format')
"
```

**5. "ADK import errors"**
```bash
# Verify ADK installation
pip install google-adk --upgrade
python -c "import google.adk; print('ADK OK')"

# Check MCPToolset specifically
python -c "from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset; print('MCPToolset OK')"
```

**6. "Go version compatibility"**
```bash
# github-mcp-server requires Go 1.23+
go version

# Update Go if needed
# Visit https://golang.org/dl/ for latest version
```

### Debugging Steps

**Step 1: Verify Prerequisites**
```bash
# Check all prerequisites
echo "=== Checking Prerequisites ==="
echo "Go version:"
go version
echo "github-mcp-server location:"
which github-mcp-server
echo "ADK installation:"
pip show google-adk
```

**Step 2: Test github-mcp-server Standalone**
```bash
# Set up minimal test
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token_here"
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}' | github-mcp-server stdio
```

**Step 3: Test MCPToolset Connection**
```python
# Test MCPToolset tách riêng
import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

async def test_connection():
    toolset = MCPToolset(
        connection_params=StdioServerParameters(
            command="github-mcp-server",
            args=["stdio"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": "your_token"}
        )
    )
    tools = await toolset.get_tools()
    print(f"Found {len(tools)} tools")
    await toolset.close()

# asyncio.run(test_connection())
```

### Performance Tips

- **Caching**: github-mcp-server caches API responses để giảm rate limiting
- **Rate Limiting**: GitHub API có [rate limits](https://docs.github.com/en/rest/rate-limit), hãy sử dụng authenticated tokens
- **Toolset Filtering**: Sử dụng `tool_filter` trong MCPToolset để chỉ load tools cần thiết
- **Environment**: Set `--read-only` flag cho github-mcp-server nếu chỉ cần read operations

### Getting Help

1. **GitHub Issues**: [github-mcp-server issues](https://github.com/github/github-mcp-server/issues)
2. **ADK Documentation**: [MCP Tools Guide](https://google.github.io/adk-docs/tools/mcp-tools/)
3. **MCP Protocol**: [Model Context Protocol Docs](https://modelcontextprotocol.io/)
4. **GitHub API**: [GitHub REST API Docs](https://docs.github.com/en/rest)

## 📁 Project Structure

```
github-mcp-agent/
├── github_agent/               # Main package
│   ├── __init__.py            # Package initialization  
│   ├── agent.py               # Main ADK agent với MCPToolset
│   ├── prompt.py              # Agent instructions & prompts
│   └── tools.py               # Custom validation & setup tools
├── pyproject.toml             # Project configuration
├── requirements.txt           # Python dependencies
├── setup.sh                   # Setup script (executable)
├── example_usage.py           # Demo usage example
└── README.md                  # Documentation
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Add tests cho changes
4. Submit Pull Request

## 📄 License

MIT License - xem LICENSE file để biết chi tiết

## 🔗 Links

- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [ADK MCP Tools Documentation](https://google.github.io/adk-docs/tools/mcp-tools/)

## 📞 Support

- Tạo issue trong repository này
- Check ADK documentation
- Review github-mcp-server documentation

---

**Phát triển bởi**: ADK Community  
**Phiên bản**: 0.1.0  
**Ngôn ngữ**: Vietnamese / Tiếng Việt 🇻🇳 