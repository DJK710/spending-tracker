#!/bin/bash

echo "Starting PostgreSQL..."
sudo service postgresql start

echo "Starting backend..."
cd backend
source ./venv/bin/activate
uvicorn app.main:app --reload &
BACKEND_PID=$!

echo "Starting frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Backend running on http://localhost:8000"
echo "Frontend running on http://localhost:5173"
echo ""
echo "Press CTRL+C to stop everything."

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

wait