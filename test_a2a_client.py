"""
Test Client cho GitHub Agent A2A Integration
Demo cách giao tiếp với GitHub Agent thông qua A2A Protocol
"""
import asyncio
import json
from a2a.client import A2AClient
from a2a.types import Message, TextContent, MessageRole


async def test_github_agent_a2a():
    """
    Test GitHub Agent thông qua A2A Protocol
    """
    print("🚀 Testing GitHub Agent A2A Integration...")
    
    # Tạo A2A client
    client = A2AClient("http://localhost:10003")
    
    # Test cases
    test_cases = [
        {
            "name": "Agent Info Request",
            "message": "Xin chào! Bạn có thể giới thiệu về GitHub Agent không?"
        },
        {
            "name": "GitHub URL Request",
            "message": "Tôi muốn làm việc với repository https://github.com/microsoft/vscode"
        },
        {
            "name": "Multiple GitHub Operations",
            "message": "Hãy giúp tôi clone repository https://github.com/facebook/react và xem thông tin về repository đó."
        },
        {
            "name": "A2A Collaboration Test",
            "message": "Tôi cần phân tích code trong repository GitHub và cần delegate task này cho specialized analysis agent. Bạn có thể giúp không?"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"📋 Test Case {i}: {test_case['name']}")
        print(f"💬 Message: {test_case['message']}")
        print("📤 Sending to GitHub Agent via A2A...")
        
        try:
            # Tạo A2A message
            message = Message(
                content=TextContent(text=test_case['message']),
                role=MessageRole.USER
            )
            
            # Gửi message thông qua A2A protocol
            response = await client.send_message_async(message)
            
            print("📥 Response received:")
            if hasattr(response, 'content') and hasattr(response.content, 'text'):
                print(f"✅ {response.content.text}")
            else:
                print(f"✅ {response}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("🎉 A2A Integration Test Complete!")


def test_sync_github_agent_a2a():
    """
    Synchronous test GitHub Agent thông qua A2A Protocol
    """
    print("🚀 Testing GitHub Agent A2A Integration (Sync)...")
    
    # Tạo A2A client
    client = A2AClient("http://localhost:10003")
    
    # Simple test
    try:
        print("\n📤 Sending simple message...")
        
        message = Message(
            content=TextContent(text="Xin chào GitHub Agent! Bạn có thể giúp tôi làm việc với GitHub không?"),
            role=MessageRole.USER
        )
        
        response = client.send_message(message)
        
        print("📥 Response:")
        if hasattr(response, 'content') and hasattr(response.content, 'text'):
            print(f"✅ {response.content.text}")
        else:
            print(f"✅ {response}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_multi_agent_scenario():
    """
    Test scenario với multiple agents (simulation)
    """
    print("\n🌐 Testing Multi-Agent Scenario...")
    
    # GitHub Agent client
    github_client = A2AClient("http://localhost:10003")
    
    # Simulate workflow: GitHub data → Analysis → Report
    workflow_steps = [
        {
            "agent": "GitHub Agent",
            "client": github_client,
            "task": "Hãy lấy thông tin về repository https://github.com/microsoft/typescript và chuẩn bị data cho analysis."
        }
        # Ở đây bạn có thể thêm other agents khi có
    ]
    
    workflow_results = {}
    
    for step in workflow_steps:
        print(f"\n📋 Executing: {step['task']}")
        print(f"🤖 Agent: {step['agent']}")
        
        try:
            message = Message(
                content=TextContent(text=step['task']),
                role=MessageRole.USER
            )
            
            response = await step['client'].send_message_async(message)
            workflow_results[step['agent']] = response
            
            print(f"✅ {step['agent']} completed successfully")
            if hasattr(response, 'content') and hasattr(response.content, 'text'):
                # Chỉ show preview của response
                preview = response.content.text[:200] + "..." if len(response.content.text) > 200 else response.content.text
                print(f"📄 Preview: {preview}")
            
        except Exception as e:
            print(f"❌ Error in {step['agent']}: {e}")
    
    print(f"\n🎯 Multi-Agent Workflow Complete!")
    print(f"📊 Results from {len(workflow_results)} agents")


if __name__ == "__main__":
    print("🔥 GitHub Agent A2A Integration Test Suite")
    print("="*60)
    
    # Check if server is running
    try:
        import requests
        response = requests.get("http://localhost:10003/health", timeout=5)
        print("✅ GitHub Agent A2A Server is running!")
    except:
        print("❌ GitHub Agent A2A Server is not running!")
        print("💡 Start it with: python -m github_agent --host localhost --port 10003")
        exit(1)
    
    # Run tests
    print("\n1️⃣ Running Synchronous Tests...")
    test_sync_github_agent_a2a()
    
    print("\n2️⃣ Running Asynchronous Tests...")
    asyncio.run(test_github_agent_a2a())
    
    print("\n3️⃣ Running Multi-Agent Scenario...")
    asyncio.run(test_multi_agent_scenario())
    
    print("\n🏁 All tests completed!")
    print("💡 GitHub Agent is now ready for A2A collaboration!") 