"""
GitHub API Client để thay thế github-mcp-server
Sử dụng GitHub REST API trực tiếp với session-based PAT
"""
import requests
import json
import base64
import subprocess
import tempfile
import os
from typing import Dict, Any, List, Optional
from urllib.parse import quote, urlparse
from .session_manager import session_manager

class GitHubAPIClient:
    """Client để tương tác với GitHub API"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.base_url = "https://api.github.com"
        
    def _get_headers(self) -> Dict[str, str]:
        """Lấy headers với authentication từ session"""
        token = session_manager.get_token(self.session_id)
        if not token:
            raise ValueError(f"Session {self.session_id} không tồn tại hoặc đã hết hạn")
        
        return {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Agent/1.0"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Thực hiện HTTP request tới GitHub API"""
        headers = self._get_headers()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        response = requests.request(method, url, headers=headers, **kwargs)
        
        if response.status_code == 401:
            raise ValueError("GitHub token không hợp lệ hoặc đã hết hạn")
        elif response.status_code == 404:
            raise ValueError("Repository hoặc resource không tồn tại")
        elif response.status_code >= 400:
            raise ValueError(f"GitHub API error: {response.status_code} - {response.text}")
        
        return response.json() if response.content else {}
    
    def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Lấy thông tin repository
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            
        Returns:
            Dict chứa thông tin repository
        """
        return self._make_request("GET", f"repos/{owner}/{repo}")
    
    def get_repository_content(self, owner: str, repo: str, path: str = "", ref: str = "main") -> List[Dict[str, Any]]:
        """
        Lấy nội dung thư mục hoặc file trong repository
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            path: Đường dẫn file/folder (mặc định là root)
            ref: Branch/commit reference (mặc định là main)
            
        Returns:
            List chứa thông tin files/folders
        """
        endpoint = f"repos/{owner}/{repo}/contents/{path}"
        params = {"ref": ref} if ref != "main" else {}
        
        result = self._make_request("GET", endpoint, params=params)
        
        # Nếu là single file, wrap trong list
        if isinstance(result, dict):
            return [result]
        return result
    
    def get_file_content(self, owner: str, repo: str, path: str, ref: str = "main") -> Dict[str, Any]:
        """
        Lấy nội dung của một file cụ thể
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            path: Đường dẫn tới file
            ref: Branch/commit reference
            
        Returns:
            Dict chứa thông tin và nội dung file
        """
        endpoint = f"repos/{owner}/{repo}/contents/{path}"
        params = {"ref": ref} if ref != "main" else {}
        
        result = self._make_request("GET", endpoint, params=params)
        
        # Decode base64 content nếu có
        if "content" in result and result["encoding"] == "base64":
            try:
                result["decoded_content"] = base64.b64decode(result["content"]).decode('utf-8')
            except UnicodeDecodeError:
                result["decoded_content"] = "[Binary file - không thể hiển thị]"
        
        return result
    
    def search_code(self, query: str, owner: str = "", repo: str = "") -> Dict[str, Any]:
        """
        Tìm kiếm code trong repository
        
        Args:
            query: Từ khóa tìm kiếm
            owner: Tên owner (optional)
            repo: Tên repository (optional)
            
        Returns:
            Dict chứa kết quả tìm kiếm
        """
        # Tạo query string
        search_query = query
        if owner and repo:
            search_query += f" repo:{owner}/{repo}"
        
        endpoint = "search/code"
        params = {"q": search_query}
        
        return self._make_request("GET", endpoint, params=params)
    
    def list_branches(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """
        Liệt kê các branch của repository
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            
        Returns:
            List chứa thông tin các branch
        """
        return self._make_request("GET", f"repos/{owner}/{repo}/branches")
    
    def list_commits(self, owner: str, repo: str, sha: str = "", path: str = "", per_page: int = 30) -> List[Dict[str, Any]]:
        """
        Liệt kê commits của repository
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            sha: SHA của commit/branch để lấy commits
            path: Đường dẫn file để lọc commits
            per_page: Số commits trên mỗi page
            
        Returns:
            List chứa thông tin commits
        """
        endpoint = f"repos/{owner}/{repo}/commits"
        params = {"per_page": per_page}
        if sha:
            params["sha"] = sha
        if path:
            params["path"] = path
            
        return self._make_request("GET", endpoint, params=params)
    
    def get_commit(self, owner: str, repo: str, sha: str) -> Dict[str, Any]:
        """
        Lấy thông tin chi tiết của một commit
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            sha: SHA của commit
            
        Returns:
            Dict chứa thông tin chi tiết commit
        """
        return self._make_request("GET", f"repos/{owner}/{repo}/commits/{sha}")
    
    def list_pull_requests(self, owner: str, repo: str, state: str = "open", per_page: int = 30) -> List[Dict[str, Any]]:
        """
        Liệt kê pull requests
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            state: Trạng thái PR (open, closed, all)
            per_page: Số PR trên mỗi page
            
        Returns:
            List chứa thông tin pull requests
        """
        endpoint = f"repos/{owner}/{repo}/pulls"
        params = {"state": state, "per_page": per_page}
        
        return self._make_request("GET", endpoint, params=params)
    
    def get_pull_request(self, owner: str, repo: str, number: int) -> Dict[str, Any]:
        """
        Lấy thông tin chi tiết của một pull request
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            number: Số của pull request
            
        Returns:
            Dict chứa thông tin chi tiết pull request
        """
        return self._make_request("GET", f"repos/{owner}/{repo}/pulls/{number}")
    
    def clone_repository(self, owner: str, repo: str, destination_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Clone repository về local sử dụng git command với token
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            destination_path: Đường dẫn đích (optional)
            
        Returns:
            Dict chứa thông tin về quá trình clone
        """
        try:
            token = session_manager.get_token(self.session_id)
            if not token:
                return {"success": False, "error": "Session không tồn tại"}
            
            # Tạo destination path nếu không được cung cấp
            if destination_path is None:
                destination_path = tempfile.mkdtemp()
            
            repo_path = os.path.join(destination_path, repo)
            
            # Tạo URL với token để clone
            clone_url = f"https://{token}@github.com/{owner}/{repo}.git"
            
            # Thực hiện git clone
            result = subprocess.run(
                ["git", "clone", clone_url, repo_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Repository đã được clone thành công",
                    "local_path": repo_path,
                    "clone_url": f"https://github.com/{owner}/{repo}.git"
                }
            else:
                return {
                    "success": False,
                    "error": f"Lỗi khi clone repository: {result.stderr}"
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Clone repository timeout (quá 5 phút)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Lỗi không xác định: {str(e)}"
            }
    
    def list_issues(self, owner: str, repo: str, state: str = "open", per_page: int = 30) -> List[Dict[str, Any]]:
        """
        Liệt kê issues của repository
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            state: Trạng thái issue (open, closed, all)
            per_page: Số issue trên mỗi page
            
        Returns:
            List chứa thông tin issues
        """
        endpoint = f"repos/{owner}/{repo}/issues"
        params = {"state": state, "per_page": per_page}
        
        return self._make_request("GET", endpoint, params=params)
    
    def get_issue(self, owner: str, repo: str, number: int) -> Dict[str, Any]:
        """
        Lấy thông tin chi tiết của một issue
        
        Args:
            owner: Tên owner của repository
            repo: Tên repository
            number: Số của issue
            
        Returns:
            Dict chứa thông tin chi tiết issue
        """
        return self._make_request("GET", f"repos/{owner}/{repo}/issues/{number}")


def create_github_client(session_id: str) -> GitHubAPIClient:
    """
    Factory function để tạo GitHub API client
    
    Args:
        session_id: ID của session
        
    Returns:
        GitHubAPIClient instance
    """
    return GitHubAPIClient(session_id) 