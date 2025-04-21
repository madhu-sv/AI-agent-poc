#!/bin/bash

echo "🔧 Setting up AI Job Agent dependencies..."

# 1. Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "🚨 Homebrew not found. Please install Homebrew first: https://brew.sh/"
    exit 1
fi

# 2. Install Homebrew dependencies
echo "📦 Installing Homebrew packages..."
brew install libmagic tesseract

# 3. Create virtual environment
echo "🧪 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install Python dependencies
echo "📦 Installing Python packages..."
pip install -r requirements.txt

echo "✅ Installation complete! To activate your environment, run:"
echo "source venv/bin/activate"