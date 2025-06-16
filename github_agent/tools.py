"""
New GitHub Tools sử dụng session-based GitHub API Client
Thay thế cho github-mcp-server để hỗ trợ multi-user
"""
import json
import re
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse
from .session_manager import session_manager
from .github_api_client import create_github_client


def validate_github_url(url: str) -> Dict[str, Any]:
    """
    Validate GitHub URL và extract owner/repo information
    
    Args:
        url: GitHub repository URL
        
    Returns:
        Dict chứa thông tin validation và parsed data
    """
    try:
        # Clean up URL
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Parse URL
        parsed = urlparse(url)
        
        if parsed.netloc.lower() not in ['github.com', 'www.github.com']:
            return {
                "valid": False,
                "error": "URL không phải của GitHub.com",
                "url": url
            }
            
        # Extract owner/repo từ path
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            return {
                "valid": False,
                "error": "URL thiếu thông tin owner hoặc repository name",
                "url": url
            }
            
        owner = path_parts[0]
        repo = path_parts[1]
        
        # Remove .git suffix if present
        if repo.endswith('.git'):
            repo = repo[:-4]
            
        return {
            "valid": True,
            "owner": owner,
            "repo": repo,
            "url": url,
            "clean_url": f"https://github.com/{owner}/{repo}"
        }
        
    except Exception as e:
        return {
            "valid": False,
            "error": f"Lỗi khi parse URL: {str(e)}",
            "url": url
        }


def validate_github_token(token: str) -> Dict[str, Any]:
    """
    Validate GitHub Personal Access Token format
    
    Args:
        token: GitHub Personal Access Token
        
    Returns:
        Dict chứa thông tin validation
    """
    try:
        token = token.strip()
        
        # Check basic format
        if not token:
            return {
                "valid": False,
                "error": "Token không được để trống"
            }
            
        # GitHub tokens có format khác nhau:
        # - Classic: ghp_xxxx (40 chars total)
        # - Fine-grained: github_pat_xxxx
        if not (token.startswith('ghp_') or token.startswith('github_pat_')):
            return {
                "valid": False,
                "error": "Token không đúng format GitHub. Token phải bắt đầu với 'ghp_' hoặc 'github_pat_'"
            }
            
        if token.startswith('ghp_') and len(token) != 40:
            return {
                "valid": False,
                "error": "Classic GitHub token phải có đúng 40 ký tự"
            }
            
        return {
            "valid": True,
            "token_type": "classic" if token.startswith('ghp_') else "fine-grained",
            "message": "Token format hợp lệ"
        }
        
    except Exception as e:
        return {
            "valid": False,
            "error": f"Lỗi khi validate token: {str(e)}"
        }


def create_github_session(github_url: str, token: str) -> str:
    """
    Tạo session mới và lưu trữ PAT cho user
    
    Args:
        github_url: GitHub repository URL
        token: GitHub Personal Access Token
        
    Returns:
        JSON string chứa thông tin session
    """
    try:
        # Validate inputs
        url_validation = validate_github_url(github_url)
        if not url_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": f"GitHub URL không hợp lệ: {url_validation['error']}"
            }, ensure_ascii=False)
            
        token_validation = validate_github_token(token)
        if not token_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": f"GitHub token không hợp lệ: {token_validation['error']}"
            }, ensure_ascii=False)
        
        # Tạo session mới
        session_id = session_manager.create_session(github_url, token)
        
        # Test connection để đảm bảo token hoạt động
        try:
            client = create_github_client(session_id)
            repo_info = client.get_repository_info(url_validation["owner"], url_validation["repo"])
            
            # Cập nhật thông tin session với repo info
            session_manager.update_session(session_id, 
                owner=url_validation["owner"],
                repo=url_validation["repo"],
                repo_full_name=repo_info.get("full_name"),
                repo_description=repo_info.get("description")
            )
            
            return json.dumps({
                "success": True,
                "session_id": session_id,
                "message": "Session đã được tạo thành công",
                "repository": {
                    "owner": url_validation["owner"],
                    "repo": url_validation["repo"],
                    "full_name": repo_info.get("full_name"),
                    "description": repo_info.get("description"),
                    "stars": repo_info.get("stargazers_count"),
                    "language": repo_info.get("language")
                }
            }, ensure_ascii=False)
            
        except Exception as api_error:
            # Xóa session nếu không thể kết nối
            session_manager.delete_session(session_id)
            return json.dumps({
                "success": False,
                "error": f"Không thể kết nối tới GitHub với token này: {str(api_error)}"
            }, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi tạo session: {str(e)}"
        }, ensure_ascii=False)


def get_repository_info_session(session_id: str) -> str:
    """
    Lấy thông tin repository sử dụng session
    
    Args:
        session_id: ID của session
        
    Returns:
        JSON string chứa thông tin repository
    """
    try:
        session_info = session_manager.get_session_info(session_id)
        if not session_info:
            return json.dumps({
                "success": False,
                "error": "Session không tồn tại hoặc đã hết hạn"
            }, ensure_ascii=False)
        
        client = create_github_client(session_id)
        
        # Parse owner/repo từ GitHub URL
        url_validation = validate_github_url(session_info["github_url"])
        if not url_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": "GitHub URL trong session không hợp lệ"
            }, ensure_ascii=False)
        
        repo_info = client.get_repository_info(url_validation["owner"], url_validation["repo"])
        
        return json.dumps({
            "success": True,
            "repository": repo_info
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi lấy thông tin repository: {str(e)}"
        }, ensure_ascii=False)


def clone_repository_session(session_id: str, destination_path: Optional[str] = None) -> str:
    """
    Clone repository sử dụng session
    
    Args:
        session_id: ID của session
        destination_path: Đường dẫn đích (optional)
        
    Returns:
        JSON string chứa thông tin về quá trình clone
    """
    try:
        session_info = session_manager.get_session_info(session_id)
        if not session_info:
            return json.dumps({
                "success": False,
                "error": "Session không tồn tại hoặc đã hết hạn"
            }, ensure_ascii=False)
        
        client = create_github_client(session_id)
        
        # Parse owner/repo từ GitHub URL
        url_validation = validate_github_url(session_info["github_url"])
        if not url_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": "GitHub URL trong session không hợp lệ"
            }, ensure_ascii=False)
        
        result = client.clone_repository(
            url_validation["owner"], 
            url_validation["repo"], 
            destination_path
        )
        
        return json.dumps(result, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi clone repository: {str(e)}"
        }, ensure_ascii=False)


def get_repository_content_session(session_id: str, path: str = "", ref: str = "main") -> str:
    """
    Lấy nội dung thư mục/file trong repository sử dụng session
    
    Args:
        session_id: ID của session
        path: Đường dẫn file/folder (mặc định là root)
        ref: Branch/commit reference (mặc định là main)
        
    Returns:
        JSON string chứa thông tin files/folders
    """
    try:
        session_info = session_manager.get_session_info(session_id)
        if not session_info:
            return json.dumps({
                "success": False,
                "error": "Session không tồn tại hoặc đã hết hạn"
            }, ensure_ascii=False)
        
        client = create_github_client(session_id)
        
        # Parse owner/repo từ GitHub URL
        url_validation = validate_github_url(session_info["github_url"])
        if not url_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": "GitHub URL trong session không hợp lệ"
            }, ensure_ascii=False)
        
        content = client.get_repository_content(
            url_validation["owner"], 
            url_validation["repo"], 
            path, 
            ref
        )
        
        return json.dumps({
            "success": True,
            "content": content
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi lấy nội dung repository: {str(e)}"
        }, ensure_ascii=False)


def get_file_content_session(session_id: str, path: str, ref: str = "main") -> str:
    """
    Lấy nội dung file cụ thể trong repository sử dụng session
    
    Args:
        session_id: ID của session
        path: Đường dẫn tới file
        ref: Branch/commit reference
        
    Returns:
        JSON string chứa nội dung file
    """
    try:
        session_info = session_manager.get_session_info(session_id)
        if not session_info:
            return json.dumps({
                "success": False,
                "error": "Session không tồn tại hoặc đã hết hạn"
            }, ensure_ascii=False)
        
        client = create_github_client(session_id)
        
        # Parse owner/repo từ GitHub URL
        url_validation = validate_github_url(session_info["github_url"])
        if not url_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": "GitHub URL trong session không hợp lệ"
            }, ensure_ascii=False)
        
        file_info = client.get_file_content(
            url_validation["owner"], 
            url_validation["repo"], 
            path, 
            ref
        )
        
        return json.dumps({
            "success": True,
            "file": file_info
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi lấy nội dung file: {str(e)}"
        }, ensure_ascii=False)


def list_pull_requests_session(session_id: str, state: str = "open", per_page: int = 10) -> str:
    """
    Liệt kê pull requests sử dụng session
    
    Args:
        session_id: ID của session
        state: Trạng thái PR (open, closed, all)
        per_page: Số PR trên mỗi page
        
    Returns:
        JSON string chứa danh sách pull requests
    """
    try:
        session_info = session_manager.get_session_info(session_id)
        if not session_info:
            return json.dumps({
                "success": False,
                "error": "Session không tồn tại hoặc đã hết hạn"
            }, ensure_ascii=False)
        
        client = create_github_client(session_id)
        
        # Parse owner/repo từ GitHub URL
        url_validation = validate_github_url(session_info["github_url"])
        if not url_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": "GitHub URL trong session không hợp lệ"
            }, ensure_ascii=False)
        
        pull_requests = client.list_pull_requests(
            url_validation["owner"], 
            url_validation["repo"], 
            state, 
            per_page
        )
        
        return json.dumps({
            "success": True,
            "pull_requests": pull_requests,
            "count": len(pull_requests)
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi lấy danh sách pull requests: {str(e)}"
        }, ensure_ascii=False)


def get_pull_request_session(session_id: str, number: int) -> str:
    """
    Lấy thông tin chi tiết pull request sử dụng session
    
    Args:
        session_id: ID của session
        number: Số của pull request
        
    Returns:
        JSON string chứa thông tin chi tiết pull request
    """
    try:
        session_info = session_manager.get_session_info(session_id)
        if not session_info:
            return json.dumps({
                "success": False,
                "error": "Session không tồn tại hoặc đã hết hạn"
            }, ensure_ascii=False)
        
        client = create_github_client(session_id)
        
        # Parse owner/repo từ GitHub URL
        url_validation = validate_github_url(session_info["github_url"])
        if not url_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": "GitHub URL trong session không hợp lệ"
            }, ensure_ascii=False)
        
        pull_request = client.get_pull_request(
            url_validation["owner"], 
            url_validation["repo"], 
            number
        )
        
        return json.dumps({
            "success": True,
            "pull_request": pull_request
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi lấy thông tin pull request: {str(e)}"
        }, ensure_ascii=False)


def get_pull_request_diff_session(session_id: str, number: int) -> str:
    """
    Lấy diff của pull request sử dụng session, output dạng markdown
    
    Args:
        session_id: ID của session
        number: Số của pull request
        
    Returns:
        String chứa diff formatted dạng markdown
    """
    try:
        session_info = session_manager.get_session_info(session_id)
        if not session_info:
            return json.dumps({
                "success": False,
                "error": "Session không tồn tại hoặc đã hết hạn"
            }, ensure_ascii=False)
        
        client = create_github_client(session_id)
        
        # Parse owner/repo từ GitHub URL
        url_validation = validate_github_url(session_info["github_url"])
        if not url_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": "GitHub URL trong session không hợp lệ"
            }, ensure_ascii=False)
        
        # Lấy thông tin PR trước
        pr_info = client.get_pull_request(
            url_validation["owner"], 
            url_validation["repo"], 
            number
        )
        
        # Lấy diff của PR
        diff_content = client.get_pull_request_diff(
            url_validation["owner"], 
            url_validation["repo"], 
            number
        )
        
        # Format thành markdown
        markdown_output = f"""# Pull Request #{number}: {pr_info.get('title', 'N/A')}

## Thông tin chi tiết
- **Trạng thái**: {pr_info.get('state', 'N/A')}
- **Người tạo**: {pr_info.get('user', {}).get('login', 'N/A')}
- **Ngày tạo**: {pr_info.get('created_at', 'N/A')}
- **Ngày cập nhật**: {pr_info.get('updated_at', 'N/A')}
- **Commits**: {pr_info.get('commits', 'N/A')}
- **Additions**: +{pr_info.get('additions', 'N/A')}
- **Deletions**: -{pr_info.get('deletions', 'N/A')}
- **Changed files**: {pr_info.get('changed_files', 'N/A')}

## Mô tả
{pr_info.get('body', 'Không có mô tả')}

## Changes (Diff)

```diff
{diff_content}
```

[Xem trên GitHub]({pr_info.get('html_url', '#')})
"""
        
        return markdown_output
        
    except Exception as e:
        return f"❌ **Lỗi khi lấy diff pull request**: {str(e)}"


def search_code_session(session_id: str, query: str) -> str:
    """
    Tìm kiếm code trong repository sử dụng session
    
    Args:
        session_id: ID của session
        query: Từ khóa tìm kiếm
        
    Returns:
        JSON string chứa kết quả tìm kiếm
    """
    try:
        session_info = session_manager.get_session_info(session_id)
        if not session_info:
            return json.dumps({
                "success": False,
                "error": "Session không tồn tại hoặc đã hết hạn"
            }, ensure_ascii=False)
        
        client = create_github_client(session_id)
        
        # Parse owner/repo từ GitHub URL
        url_validation = validate_github_url(session_info["github_url"])
        if not url_validation["valid"]:
            return json.dumps({
                "success": False,
                "error": "GitHub URL trong session không hợp lệ"
            }, ensure_ascii=False)
        
        search_results = client.search_code(
            query, 
            url_validation["owner"], 
            url_validation["repo"]
        )
        
        return json.dumps({
            "success": True,
            "search_results": search_results
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi tìm kiếm code: {str(e)}"
        }, ensure_ascii=False)


def list_sessions() -> str:
    """
    Liệt kê tất cả session hiện tại
    
    Returns:
        JSON string chứa danh sách sessions
    """
    try:
        sessions = session_manager.list_sessions()
        return json.dumps({
            "success": True,
            "sessions": sessions,
            "count": len(sessions)
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi liệt kê sessions: {str(e)}"
        }, ensure_ascii=False)


def cleanup_expired_sessions(max_age_hours: int = 24) -> str:
    """
    Xóa các session hết hạn
    
    Args:
        max_age_hours: Thời gian tối đa session được giữ (giờ)
        
    Returns:
        JSON string chứa thông tin cleanup
    """
    try:
        cleaned_count = session_manager.cleanup_expired_sessions(max_age_hours)
        return json.dumps({
            "success": True,
            "message": f"Đã xóa {cleaned_count} session hết hạn",
            "cleaned_count": cleaned_count
        }, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Lỗi khi cleanup sessions: {str(e)}"
        }, ensure_ascii=False)


def show_github_setup_guide() -> str:
    """
    Hiển thị hướng dẫn setup GitHub Personal Access Token
    
    Returns:
        String chứa hướng dẫn setup
    """
    return """
# 🔧 Hướng dẫn thiết lập GitHub Personal Access Token

## Bước 1: Truy cập GitHub Settings
1. Đăng nhập vào GitHub.com
2. Click vào avatar của bạn ở góc phải trên
3. Chọn **Settings**

## Bước 2: Tạo Personal Access Token
1. Trong sidebar bên trái, chọn **Developer settings**
2. Chọn **Personal access tokens** > **Tokens (classic)**
3. Click **Generate new token** > **Generate new token (classic)**

## Bước 3: Cấu hình Token
1. **Note**: Nhập mô tả cho token (ví dụ: "ADK GitHub Agent")
2. **Expiration**: Chọn thời hạn (khuyến nghị: 90 days)
3. **Select scopes**: Chọn các quyền cần thiết:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **read:org** (Read org and team membership)
   - ✅ **user:email** (Access user email addresses)
   - ✅ **workflow** (Update GitHub Action workflows) - nếu cần

## Bước 4: Tạo và Lưu Token
1. Click **Generate token**
2. **⚠️ QUAN TRỌNG**: Copy token ngay lập tức và lưu vào nơi an toàn
3. Bạn sẽ không thể xem lại token này!

## Bước 5: Sử dụng Token
- Token sẽ có dạng: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- Giữ token này bí mật, không chia sẻ với ai
- Sử dụng token này khi agent hỏi về GITHUB_PERSONAL_ACCESS_TOKEN

## Bước 6: Sau khi có token
1. Cung cấp GitHub repository URL (ví dụ: https://github.com/owner/repo)
2. Cung cấp token khi được yêu cầu
3. Agent sẽ tạo session và cho phép sử dụng GitHub tools

## 🔒 Lưu ý bảo mật:
- Không commit token vào code
- Không chia sẻ token trên chat/email
- Revoke token nếu nghi ngờ bị lộ
- Sử dụng token với expiration date hợp lý
- Monitor token usage qua GitHub Settings

## 🚀 GitHub Tools có sẵn:
Sau khi tạo session, bạn có thể sử dụng các tools sau:
- **get_repository_info_session**: Lấy thông tin repository
- **get_repository_content_session**: Xem nội dung files/folders
- **get_file_content_session**: Đọc nội dung file cụ thể
- **list_pull_requests_session**: Liệt kê pull requests
- **get_pull_request_session**: Chi tiết pull request
- **search_code_session**: Tìm kiếm code
- **clone_repository_session**: Clone repository
- Và nhiều tools khác...
    """.strip() 