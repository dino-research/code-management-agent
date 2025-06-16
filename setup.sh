#!/bin/bash

# GitHub Agent Setup Script
echo "🚀 GitHub Agent Setup Script"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if Python 3.11+ is installed
print_status "Checking Python version..."
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    print_status "Python $python_version is installed ✓"
else
    print_error "Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

# Check if Google Cloud CLI is installed
print_status "Checking Google Cloud CLI..."
if command -v gcloud &> /dev/null; then
    print_status "Google Cloud CLI is installed ✓"
else
    print_warning "Google Cloud CLI is not installed. Please install it:"
    echo "  Follow: https://cloud.google.com/sdk/docs/install"
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created ✓"
else
    print_status "Virtual environment already exists ✓"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

print_status "Python dependencies installed ✓"

# Check Google Cloud authentication
print_status "Checking Google Cloud authentication..."
if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    print_status "Google Cloud authentication is active ✓"
else
    print_warning "Google Cloud authentication not found."
    print_warning "Please run: gcloud auth application-default login"
fi

# Print setup completion
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Set your Google Cloud environment variables:"
echo "   export GOOGLE_GENAI_USE_VERTEXAI=true"
echo "   export GOOGLE_CLOUD_PROJECT=<your-project-id>"
echo "   export GOOGLE_CLOUD_LOCATION=<your-location>"
echo ""
echo "2. Authenticate with Google Cloud (if not done):"
echo "   gcloud auth application-default login"
echo ""
echo "3. Run the agent:"
echo "   source venv/bin/activate"
echo "   adk web"
echo ""
echo "4. Open browser at http://localhost:8000 and select 'github_agent'"
echo ""
echo "🔧 Session-based GitHub Agent features:"
echo "   - Multi-user support with session isolation"
echo "   - Direct GitHub API integration"
echo "   - Dynamic Personal Access Token setup"
echo "   - Automatic session cleanup"
echo ""
echo "📚 For more information, see README.md" 