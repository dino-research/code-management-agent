"""
CLI Entry point cho GitHub Agent A2A Server
Chạy GitHub Agent như A2A Server để giao tiếp với other agents
"""
import logging
import os
import click
import uvicorn
from dotenv import load_dotenv

from .a2a_server import create_github_a2a_server

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', default='localhost', help='Host để bind server')
@click.option('--port', default=10003, help='Port để bind server') 
@click.option('--debug', is_flag=True, help='Enable debug mode')
def main(host: str, port: int, debug: bool):
    """
    🚀 Khởi động GitHub Agent A2A Server
    
    Server này cho phép GitHub Agent giao tiếp với other agents thông qua A2A Protocol.
    
    Ví dụ:
        python -m github_agent --host 0.0.0.0 --port 10003
    """
    try:
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")
        
        logger.info("🚀 Khởi động GitHub Agent A2A Server...")
        logger.info(f"📍 Server sẽ chạy tại: http://{host}:{port}")
        logger.info("🔗 A2A endpoint: http://{host}:{port}/a2a")
        
        # Tạo A2A server instance
        server = create_github_a2a_server(host=host, port=port)
        app = server.build()
        
        logger.info("✅ GitHub Agent A2A Server đã sẵn sàng!")
        logger.info("📋 Skills available:")
        logger.info("  - GitHub Repository Management")
        logger.info("  - Pull Request Management")
        logger.info("  - Code Search and Analysis")
        logger.info("  - Session Management")
        
        # Chạy server
        uvicorn.run(
            app, 
            host=host, 
            port=port, 
            log_level='debug' if debug else 'info'
        )
        
    except KeyboardInterrupt:
        logger.info("👋 Dừng GitHub Agent A2A Server...")
    except Exception as e:
        logger.error(f"❌ Lỗi khi khởi động server: {e}")
        if debug:
            raise
        exit(1)


if __name__ == '__main__':
    main() 