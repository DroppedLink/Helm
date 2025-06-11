#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Checking NATS system setup..."

# Check if NATS container is running
if ! docker ps | grep -q "helm-nats-bus"; then
    echo -e "${RED}Error: NATS container (helm-nats-bus) is not running!${NC}"
    echo "Please start the NATS service using:"
    echo "cd .. && docker-compose -f nats-compose.yml up -d"
    exit 1
fi

# Check if required ports are accessible
if ! nc -z -w5 localhost 4222; then
    echo -e "${RED}Error: NATS client port (4222) is not accessible!${NC}"
    exit 1
fi

if ! nc -z -w5 localhost 8222; then
    echo -e "${RED}Error: NATS monitoring port (8222) is not accessible!${NC}"
    exit 1
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed!${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the tests
echo -e "${GREEN}Running NATS system tests...${NC}"
python3 test_nats_setup.py

# Deactivate virtual environment
deactivate