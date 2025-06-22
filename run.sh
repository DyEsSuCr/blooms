#!/bin/bash

set -e

if [ ! -f ".venv/bin/activate" ]; then
    echo "❌ Virtual environment not found at .venv/bin/activate"
    exit 1
fi

source .venv/bin/activate

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

run_step() {
    echo ">>> $1..."
    start=$(date +%s)
    if eval "$2"; then
        end=$(date +%s)
        echo -e "${GREEN}✅ $1 completed in $((end - start)) seconds.${NC}"
    else
        echo -e "${RED}❌ Error during $1 (exit code $?)${NC}"
        exit 1
    fi
}

run_step "Running spiders" "python run_spiders.py"
run_step "Running analysis" "python run_llm.py"
run_step "Starting server" "streamlit run run_server.py"
