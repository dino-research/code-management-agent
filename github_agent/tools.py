"""
Custom tools để tương tác với GitHub repository
"""
import re
import os
import subprocess
import tempfile
from typing import Dict, Any, Optional
from urllib.parse import urlparse


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


def setup_github_environment(github_url: str, token: str) -> Dict[str, Any]:
    """
    Setup environment cho github-mcp-server và ADK
    
    Args:
        github_url: GitHub repository URL
        token: GitHub Personal Access Token
        
    Returns:
        Dict chứa thông tin setup
    """
    try:
        # Validate inputs
        url_validation = validate_github_url(github_url)
        if not url_validation["valid"]:
            return {
                "success": False,
                "error": f"GitHub URL không hợp lệ: {url_validation['error']}"
            }
            
        token_validation = validate_github_token(token)
        if not token_validation["valid"]:
            return {
                "success": False,
                "error": f"GitHub token không hợp lệ: {token_validation['error']}"
            }
            
        # Set environment variables for github-mcp-server
        # Đây là cách github-mcp-server expect environment variable
        os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'] = token
        
        # Lưu thông tin cho session (để có thể reference sau này)
        repository_info = {
            "owner": url_validation["owner"],
            "repo": url_validation["repo"],
            "clean_url": url_validation["clean_url"],
            "token_type": token_validation["token_type"]
        }
        
        return {
            "success": True,
            "message": "Environment đã được setup thành công cho github-mcp-server",
            "repository": repository_info,
            "note": "Bây giờ bạn có thể sử dụng các GitHub MCP tools để tương tác với repository"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Lỗi khi setup environment: {str(e)}"
        }


def clone_repository(github_url: str, destination_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Clone GitHub repository về local (alternative method)
    
    Args:
        github_url: GitHub repository URL
        destination_path: Đường dẫn để clone (optional)
        
    Returns:
        Dict chứa thông tin về quá trình clone
    """
    try:
        # Validate GitHub URL
        url_validation = validate_github_url(github_url)
        if not url_validation["valid"]:
            return {
                "success": False,
                "error": f"GitHub URL không hợp lệ: {url_validation['error']}"
            }
            
        # Prepare destination
        if destination_path is None:
            destination_path = tempfile.mkdtemp()
            
        repo_path = os.path.join(destination_path, url_validation["repo"])
        
        # Check if token is available
        token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
        if not token:
            return {
                "success": False,
                "error": "GITHUB_PERSONAL_ACCESS_TOKEN chưa được set. Hãy chạy setup_github_environment trước."
            }
            
        # Prepare clone URL with authentication
        clone_url = f"https://{token}@github.com/{url_validation['owner']}/{url_validation['repo']}.git"
        
        # Execute git clone
        result = subprocess.run(
            ['git', 'clone', clone_url, repo_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "repo_path": repo_path,
                "owner": url_validation["owner"],
                "repo": url_validation["repo"],
                "message": f"Repository đã được clone thành công vào {repo_path}"
            }
        else:
            return {
                "success": False,
                "error": f"Lỗi khi clone repository: {result.stderr}",
                "returncode": result.returncode
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Clone repository timeout (5 minutes)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Lỗi không mong đợi: {str(e)}"
        }


def get_repository_info(owner: str, repo: str) -> str:
    """
    Lấy thông tin cơ bản về repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        
    Returns:
        String chứa thông tin repository
    """
    return f"""
Repository Information:
- Owner: {owner}
- Name: {repo}
- URL: https://github.com/{owner}/{repo}

Để lấy thông tin chi tiết hơn, hãy sử dụng GitHub MCP tools sau khi setup environment.
Ví dụ: get_repository, get_repository_content, search_repositories, etc.
    """.strip()


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
3. Agent sẽ setup environment và cho phép sử dụng GitHub MCP tools

## 🔒 Lưu ý bảo mật:
- Không commit token vào code
- Không chia sẻ token trên chat/email
- Revoke token nếu nghi ngờ bị lộ
- Sử dụng token với expiration date hợp lý
- Monitor token usage qua GitHub Settings

## 🚀 GitHub MCP Tools có sẵn:
Sau khi setup, bạn có thể sử dụng các tools sau:
- **get_repository**: Lấy thông tin repository
- **get_repository_content**: Xem nội dung files/folders
- **search_repositories**: Tìm kiếm repositories
- **list_commits**: Xem lịch sử commits
- **create_branch**: Tạo branch mới
- **search_code**: Tìm kiếm code
- **get_file_contents**: Đọc nội dung file cụ thể
- **list_branches**: Liệt kê các branches
- Và nhiều tools khác...
    """.strip()


def initialize_github_mcp_connection(github_token: str, github_url: str = "") -> str:
    """
    Khởi tạo kết nối MCP với github-mcp-server sau khi có GitHub token
    
    Args:
        github_token: GitHub Personal Access Token
        github_url: GitHub repository URL (optional)
        
    Returns:
        str: Thông báo kết quả
    """
    try:
        # Validate token first
        token_validation = validate_github_token(github_token)
        if not token_validation["valid"]:
            return f"❌ Token không hợp lệ: {token_validation['error']}"
        
        # Set environment variable cho github-mcp-server
        os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = github_token
        
        # Nếu có GitHub URL, extract repo info để set thêm context
        if github_url:
            url_validation = validate_github_url(github_url)
            if url_validation["valid"]:
                owner = url_validation["owner"]
                repo = url_validation["repo"]
                os.environ["GITHUB_REPOSITORY"] = f"{owner}/{repo}"
                os.environ["GITHUB_OWNER"] = owner
                return f"✅ Đã thiết lập kết nối MCP với GitHub thành công!\n📁 Repository: {owner}/{repo}\n🔐 Token type: {token_validation['token_type']}"
            else:
                return f"✅ Đã thiết lập token MCP với GitHub thành công!\n⚠️ GitHub URL có lỗi: {url_validation['error']}\n🔐 Token type: {token_validation['token_type']}"
        else:
            return f"✅ Đã thiết lập token MCP với GitHub thành công!\n🔐 Token type: {token_validation['token_type']}\n💡 Bạn có thể cung cấp GitHub URL để có thêm context về repository."
        
    except Exception as e:
        return f"❌ Lỗi khi thiết lập kết nối MCP: {str(e)}" 