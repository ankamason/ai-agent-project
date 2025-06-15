#!/bin/bash

# AI Agent Development Environment Setup Script

echo "🚀 Activating AI Agent Development Environment..."

# Activate virtual environment
source venv/bin/activate

# Verify activation
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual environment activated: $VIRTUAL_ENV"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Display Python information
echo "📍 Python interpreter: $(which python)"
echo "🐍 Python version: $(python --version)"

# Check if python3 points to venv
if [ "$(which python)" = "$(which python3)" ]; then
    echo "✅ python3 properly configured"
else
    echo "⚠️  python3 points to: $(which python3)"
    echo "🔧 Creating python3 symlink..."
    ln -sf "$VIRTUAL_ENV/bin/python" "$VIRTUAL_ENV/bin/python3"
    echo "✅ python3 symlink created"
fi

# Test both AI agent and calculator
echo "🧪 Testing AI Agent..."
python main.py "Quick test: what is 2+2?" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ AI Agent working"
else
    echo "❌ AI Agent test failed"
fi

echo "🧮 Testing Calculator..."
cd calculator
python tests.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Calculator tests passing"
else
    echo "❌ Calculator tests failed"
fi

# Return to main directory
cd ..

echo "🎉 Development environment ready!"
echo ""
echo "Available commands:"
echo "  AI Agent: python main.py \"your question\" [--verbose]"
echo "  Calculator: cd calculator && python main.py \"3 + 5\""
echo "  Tests: cd calculator && python tests.py"
