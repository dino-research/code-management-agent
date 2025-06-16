# Migration Guide: Từ github-mcp-server sang Session-based Approach

## 🎯 Tổng quan

Dự án đã được nâng cấp từ việc sử dụng `github-mcp-server` sang **session-based approach** để giải quyết các vấn đề sau:

### ❌ Vấn đề với github-mcp-server
1. **Environment Variable Conflict**: github-mcp-server yêu cầu `GITHUB_PERSONAL_ACCESS_TOKEN` được thiết lập trong environment variable ngay khi khởi chạy
2. **Multi-user Problem**: Khi phục vụ nhiều người dùng, việc thay đổi environment variable sẽ gây xung đột giữa các session
3. **Dynamic Setup Limitation**: Không thể dynamic setup token sau khi người dùng cung cấp trong cuộc trò chuyện

### ✅ Giải pháp Session-based
1. **Session Management**: Mỗi session lưu trữ PAT riêng biệt với session ID làm key
2. **Direct GitHub API**: Sử dụng GitHub REST API trực tiếp thay vì github-mcp-server
3. **Multi-user Support**: Hỗ trợ nhiều người dùng đồng thời mà không xung đột
4. **Security**: Session tự động cleanup sau 24 giờ

## 🏗️ Kiến trúc mới

### Before (github-mcp-server)
```
User → Agent → github-mcp-server → GitHub API
               ↑
               Environment Variable (GITHUB_PERSONAL_ACCESS_TOKEN)
```

### After (Session-based)
```
User → Agent → Session Manager → GitHub API Client → GitHub API
               ↑
               Session Storage (session_id → PAT mapping)
```

## 📁 Cấu trúc file mới

```
github_agent/
├── agent.py                 # Updated: Sử dụng session-based tools
├── prompt.py                # Updated: Thêm GITHUB_AGENT_PROMPT_NEW
├── tools.py                 # Existing: Validation tools
├── session_manager.py       # NEW: Quản lý session và PAT
├── github_api_client.py     # NEW: Direct GitHub API client
├── new_tools.py            # NEW: Session-based tools
└── __init__.py
```

## 🔧 Thay đổi chính

### 1. Session Manager (session_manager.py)
- **Chức năng**: Quản lý session và lưu trữ PAT theo session ID
- **Features**:
  - Thread-safe operations
  - Automatic cleanup (24h default)
  - Session isolation

### 2. GitHub API Client (github_api_client.py)
- **Chức năng**: Tương tác trực tiếp với GitHub REST API
- **Features**:
  - Repository operations
  - File content operations
  - Pull request management
  - Code search
  - Clone repository

### 3. New Tools (new_tools.py)
- **Session-based tools**:
  - `create_github_session()`: Tạo session mới
  - `get_repository_info_session()`: Lấy thông tin repo
  - `clone_repository_session()`: Clone repository
  - `list_pull_requests_session()`: Liệt kê PRs
  - `get_pull_request_session()`: Chi tiết PR
  - `search_code_session()`: Tìm kiếm code

### 4. Updated Agent (agent.py)
- **Loại bỏ**: MCPToolset và github-mcp-server connection
- **Thêm**: Session-based tools
- **Prompt**: Sử dụng GITHUB_AGENT_PROMPT_NEW

## 🚀 Workflow mới

### 1. User Interaction Flow
```
1. User cung cấp GitHub URL
2. User cung cấp Personal Access Token
3. Agent tạo session với create_github_session()
4. Agent lưu session_id và sử dụng cho các operations tiếp theo
5. Tất cả GitHub operations sử dụng session_id
```

### 2. Session Lifecycle
```
Create Session → Use Tools → Auto Cleanup (24h)
     ↓              ↓              ↓
  Validate       Authenticate    Clean Memory
   & Store        with GitHub
```

## 🔒 Security Improvements

### Token Security
- ✅ **Session Isolation**: Mỗi user có session riêng
- ✅ **Memory Only**: Token chỉ lưu trong memory, không write ra disk
- ✅ **Auto Cleanup**: Session tự động xóa sau 24h
- ✅ **No Environment Pollution**: Không thay đổi environment variables

### Multi-user Safety
- ✅ **Concurrent Users**: Hỗ trợ nhiều user đồng thời
- ✅ **No Token Conflict**: Mỗi session có token riêng
- ✅ **Thread Safe**: Session manager thread-safe

## 📋 Migration Steps

### Cho Developers
1. **Cập nhật dependencies**:
   ```bash
   pip install -r requirements.txt  # Đã thêm requests>=2.31.0
   ```

2. **Không cần github-mcp-server nữa**:
   - Loại bỏ github-mcp-server binary
   - Không cần setup GITHUB_PERSONAL_ACCESS_TOKEN environment variable

3. **Test với ADK Web UI**:
   ```bash
   adk web
   # Chọn github_agent từ dropdown
   ```

### Cho End Users
**Không có thay đổi gì trong workflow**:
1. Cung cấp GitHub URL
2. Cung cấp Personal Access Token
3. Sử dụng agent như bình thường

## 🔄 Backwards Compatibility

### Deprecated (Sẽ bị loại bỏ)
- `setup_github_environment()`
- `initialize_github_mcp_connection()`
- MCPToolset usage
- github-mcp-server dependency

### Maintained (Vẫn hoạt động)
- `validate_github_url()`
- `validate_github_token()`
- `show_github_setup_guide()`
- Tất cả user-facing workflows

## 🧪 Testing

### Test Session Management
```python
from github_agent.session_manager import session_manager

# Test create session
session_id = session_manager.create_session("https://github.com/user/repo", "ghp_token")

# Test get token
token = session_manager.get_token(session_id)

# Test cleanup
session_manager.cleanup_expired_sessions()
```

### Test GitHub API Client
```python
from github_agent.github_api_client import create_github_client

client = create_github_client(session_id)
repo_info = client.get_repository_info("microsoft", "vscode")
```

## 🚀 Benefits

1. **Scalability**: Hỗ trợ unlimited concurrent users
2. **Security**: Token isolation và auto cleanup
3. **Reliability**: Không phụ thuộc external binary
4. **Maintainability**: Code dễ maintain và debug hơn
5. **Performance**: Direct API calls, ít overhead

## 🔮 Future Enhancements

1. **Session Persistence**: Lưu session vào database cho production
2. **Rate Limiting**: Implement rate limiting per session
3. **Audit Log**: Log activities theo session
4. **Advanced Auth**: Hỗ trợ OAuth Apps và GitHub Apps 