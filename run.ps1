# Run both Backend and Frontend in separate windows
Write-Host "Starting Agent Ai Platform..." -ForegroundColor Cyan

# Start Backend
Write-Host "-> Launching Backend (Uvicorn)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn api.main:app --reload"

# Start Frontend
Write-Host "-> Launching Frontend (Vite)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Both services are starting in new windows!" -ForegroundColor Green
