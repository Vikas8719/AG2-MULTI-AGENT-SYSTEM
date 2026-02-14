#!/bin/bash
echo "Setting up AG2 Multi-Agent System..."

# Create virtual environment
python -m venv venv
source venv/scripts/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p projects logs/agents uploads

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please configure it with your credentials."
fi

echo "Setup complete! Run: streamlit run ui/streamlit_app.py"
