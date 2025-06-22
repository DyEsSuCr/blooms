#!/bin/bash

set -e

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

LOG_SPIDERS="$LOG_DIR/spiders.log"
LOG_LLM="$LOG_DIR/llm.log"
LOG_SERVER="$LOG_DIR/server.log"

if [ ! -f ".venv/bin/activate" ]; then
    echo "❌ Virtual environment not found at .venv/bin/activate"
    exit 1
fi

source .venv/bin/activate

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

run_step() {
    local description="$1"
    local command="$2"
    local logfile="$3"

    echo ">>> $description..."
    start=$(date +%s)

    if eval "$command" >"$logfile" 2>&1; then
        end=$(date +%s)
        echo -e "${GREEN}✅ $description completed in $((end - start)) seconds.${NC}"
    else
        echo -e "${RED}❌ Error during $description (see $logfile)${NC}"
        exit 1
    fi
}

run_step "Running spiders" "python run_spiders.py" "$LOG_SPIDERS"
run_step "Running analysis" "python run_llm.py" "$LOG_LLM"

echo ">>> Starting server in background..."
start=$(date +%s)
nohup streamlit run run_server.py >"$LOG_SERVER" 2>&1 &

SERVER_PID=$!
end=$(date +%s)
echo -e "${GREEN}✅ Server started in background (PID $SERVER_PID) in $((end - start)) seconds.${NC}"
echo "📝 Logs: tail -f $LOG_SERVER"
echo "🛑 To stop the server: kill $SERVER_PID"
