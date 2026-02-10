#!/bin/bash

# Setup script for Cybersecurity Datasets Downloader
# This script sets up the Python environment and installs dependencies

set -e

echo "🛡️  Cybersecurity Datasets Downloader - Setup"
echo "================================================"
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python 3 is installed: $(python3 --version)"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed!"
    echo "   Please install Git"
    exit 1
fi

echo "✅ Git is installed: $(git --version)"
echo

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⏭️  Virtual environment already exists"
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install requirements
echo "📦 Installing requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Requirements installed"
else
    echo "⚠️  requirements.txt not found"
fi
echo

# Print usage instructions
echo "================================================"
echo "✅ Setup complete!"
echo "================================================"
echo
echo "📚 Usage Instructions:"
echo
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo
echo "  2. Download all datasets:"
echo "     python download_all.py"
echo
echo "  3. Download specific phase:"
echo "     python download_all.py --phase 1"
echo
echo "  4. Check progress:"
echo "     python check_progress.py"
echo
echo "  5. Use custom directory:"
echo "     python download_all.py --dir /path/to/datasets"
echo
echo "💡 Tip: Set NVD_API_KEY environment variable for faster CVE downloads"
echo "   export NVD_API_KEY=your_api_key_here"
echo
echo "📖 For more information, see README.md"
echo
