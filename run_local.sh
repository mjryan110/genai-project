#!/bin/bash

BACKEND_PORT=8000
FRONTEND_PORT=8501

# Kill backend if running
PID=$(lsof -ti tcp:$BACKEND_PORT)
if [ -n "$PID" ]; then
  echo "Killing process on port $BACKEND_PORT (PID: $PID)"
  kill -9 $PID
else
  echo "No process using port $BACKEND_PORT"
fi

# Kill frontend if running
PID=$(lsof -ti tcp:$FRONTEND_PORT)
if [ -n "$PID" ]; then
  echo "Killing process on port $FRONTEND_PORT (PID: $PID)"
  kill -9 $PID
else
  echo "No process using port $FRONTEND_PORT"
fi

# Start backend
echo "🚀 Starting FastAPI (Uvicorn) on port $BACKEND_PORT..."
poetry run uvicorn app.main:app --port $BACKEND_PORT --reload &

# Start frontend
echo "🧠 Launching Streamlit frontend on port $FRONTEND_PORT..."
poetry run streamlit run app/frontend/ui.py --server.port $FRONTEND_PORT
