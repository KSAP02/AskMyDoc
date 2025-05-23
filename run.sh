#!/bin/bash
# Script to start all components of AskMyDoc

# Check if the frontend directory exists
if [ ! -d "frontend" ]; then
  echo "Error: frontend directory not found!"
  exit 1
fi

# Check if the backend directory exists
if [ ! -d "backend" ]; then
  echo "Error: backend directory not found!"
  exit 1
fi

echo "Starting FastAPI backend on port 8000..."
cd backend
python main_backend.py &
BACKEND_PID=$!
echo "Backend started with PID $BACKEND_PID"
cd ..

echo "Starting Streamlit frontend on port 8501..."
cd frontend
streamlit run frontend_app.py &
STREAMLIT_PID=$!
echo "Streamlit frontend started with PID $STREAMLIT_PID"
cd ..

echo "All components are now running!"
echo "To load the extension in Chrome:"
echo "1. Open Chrome and navigate to chrome://extensions/"
echo "2. Enable 'Developer mode' (toggle in the top right)"
echo "3. Click 'Load unpacked' and select the 'extension' folder from this project"
echo "4. Open any PDF in Chrome to test the extension"
echo ""
echo "Troubleshooting:"
echo "- If the extension can't connect to localhost, make sure:"
echo "  a) FastAPI backend is running on port 8000"
echo "  b) Streamlit frontend is running on port 8501"
echo "  c) Your browser allows connections to localhost"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to press Ctrl+C
wait
