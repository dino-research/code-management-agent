"""
Session Manager để quản lý GitHub Personal Access Token theo session
"""
import uuid
from typing import Dict, Optional, Any
from threading import Lock
import time

class SessionManager:
    """Quản lý session và PAT cho từng user session"""
    
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
    
    def create_session(self, github_url: str, token: str) -> str:
        """
        Tạo session mới và lưu trữ PAT
        
        Args:
            github_url: GitHub repository URL
            token: GitHub Personal Access Token
            
        Returns:
            session_id: ID của session được tạo
        """
        session_id = str(uuid.uuid4())
        
        with self._lock:
            self._sessions[session_id] = {
                'token': token,
                'github_url': github_url,
                'created_at': time.time(),
                'last_accessed': time.time()
            }
        
        return session_id
    
    def get_token(self, session_id: str) -> Optional[str]:
        """
        Lấy PAT của session
        
        Args:
            session_id: ID của session
            
        Returns:
            token hoặc None nếu session không tồn tại
        """
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id]['last_accessed'] = time.time()
                return self._sessions[session_id]['token']
        return None
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin đầy đủ của session
        
        Args:
            session_id: ID của session
            
        Returns:
            Dict chứa thông tin session hoặc None
        """
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id]['last_accessed'] = time.time()
                return self._sessions[session_id].copy()
        return None
    
    def update_session(self, session_id: str, **kwargs) -> bool:
        """
        Cập nhật thông tin session
        
        Args:
            session_id: ID của session
            **kwargs: Các thông tin cần cập nhật
            
        Returns:
            True nếu cập nhật thành công, False nếu session không tồn tại
        """
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id].update(kwargs)
                self._sessions[session_id]['last_accessed'] = time.time()
                return True
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Xóa session
        
        Args:
            session_id: ID của session
            
        Returns:
            True nếu xóa thành công, False nếu session không tồn tại
        """
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
        return False
    
    def cleanup_expired_sessions(self, max_age_hours: int = 24) -> int:
        """
        Xóa các session hết hạn
        
        Args:
            max_age_hours: Thời gian tối đa session được giữ (giờ)
            
        Returns:
            Số session đã được xóa
        """
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        expired_sessions = []
        
        with self._lock:
            for session_id, session_data in self._sessions.items():
                if current_time - session_data['last_accessed'] > max_age_seconds:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self._sessions[session_id]
        
        return len(expired_sessions)
    
    def list_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        Liệt kê tất cả session (không bao gồm token để bảo mật)
        
        Returns:
            Dict chứa thông tin các session
        """
        with self._lock:
            return {
                session_id: {
                    'github_url': data['github_url'],
                    'created_at': data['created_at'],
                    'last_accessed': data['last_accessed']
                }
                for session_id, data in self._sessions.items()
            }

# Global session manager instance
session_manager = SessionManager() 