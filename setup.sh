#!/bin/bash

# GitHub Agent A2A Setup Script
echo "🤖 GitHub Agent A2A Setup Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

# Check if Python 3.11+ is installed
print_section "Checking Python version..."
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    print_status "Python $python_version is installed ✓"
else
    print_error "Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

# Check if Google Cloud CLI is installed
print_section "Checking Google Cloud CLI..."
if command -v gcloud &> /dev/null; then
    print_status "Google Cloud CLI is installed ✓"
else
    print_warning "Google Cloud CLI is not installed. Please install it:"
    echo "  Follow: https://cloud.google.com/sdk/docs/install"
fi

# Create virtual environment
print_section "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created ✓"
else
    print_status "Virtual environment already exists ✓"
fi

# Activate virtual environment
print_section "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_section "Installing dependencies (including A2A SDK)..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

print_status "Python dependencies installed ✓"
print_status "A2A SDK installed ✓"

# Check Google Cloud authentication
print_section "Checking Google Cloud authentication..."
if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    print_status "Google Cloud authentication is active ✓"
else
    print_warning "Google Cloud authentication not found."
    print_warning "Please run: gcloud auth application-default login"
fi

# Print setup completion
echo ""
echo "🎉 GitHub Agent A2A Setup completed successfully!"
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🤖 GitHub Agent A2A Ready                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Environment Setup:"
echo "1. Set your Google Cloud environment variables:"
echo "   export GOOGLE_GENAI_USE_VERTEXAI=true"
echo "   export GOOGLE_CLOUD_PROJECT=<your-project-id>"
echo "   export GOOGLE_CLOUD_LOCATION=<your-location>"
echo ""
echo "2. Authenticate with Google Cloud (if not done):"
echo "   gcloud auth application-default login"
echo ""
echo "🚀 Running Options:"
echo ""
echo "Option 1 - A2A Server Mode (Recommended for multi-agent systems):"
echo "   source venv/bin/activate"
echo "   python -m github_agent --host localhost --port 10003"
echo "   → GitHub Agent runs as A2A server for multi-agent communication"
echo ""
echo "Option 2 - Traditional ADK Web Mode:"
echo "   source venv/bin/activate"
echo "   adk web"
echo "   → Open browser at http://localhost:8000 and select 'github_agent'"
echo ""
echo "🔗 A2A Integration Features:"
echo "   ✅ Multi-agent communication via Agent2Agent Protocol"
echo "   ✅ Session-based GitHub API access with isolation"
echo "   ✅ Task delegation to specialized agents"
echo "   ✅ Agent discovery and collaboration"
echo "   ✅ HTTP/JSON messaging for interoperability"
echo ""
echo "🧪 Testing A2A Integration:"
echo "   # Start server in terminal 1:"
echo "   python -m github_agent --host localhost --port 10003"
echo ""
echo "   # Test from other agents or clients"
echo "   curl -X POST http://localhost:10003/ -H 'Content-Type: application/json' \\"
echo "        -d '{\"message\": \"Xin chào GitHub Agent!\"}'"
echo ""
echo "📚 For detailed A2A usage guide, see README.md" 