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
        python -m github_agent --host localhost --port 10003
        python -m github_agent --host 0.0.0.0 --port 8080 --debug
    """
    try:
        # Tạo A2A server
        app = create_github_a2a_server(host, port)
        
        # Cấu hình logging level
        log_level = "debug" if debug else "info"
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    🤖 GitHub Agent A2A Server                ║
║                                                              ║
║  🌐 Host: {host:<20} 🔌 Port: {port:<10}           ║
║  🔧 Debug: {'Enabled' if debug else 'Disabled':<18} 📊 A2A Protocol: Ready    ║
║                                                              ║
║  🚀 Server starting...                                       ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Chạy server
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level=log_level,
            access_log=debug
        )
        
    except Exception as e:
        logger.error(f"❌ Lỗi khi khởi động server: {e}")
        raise click.ClickException(f"Không thể khởi động server: {e}")


if __name__ == "__main__":
    main() 