# Zamil Full-Stack Orchestration Script
# This script sets up and runs both the Django backend and Flutter frontend locally.

$ErrorActionPreference = "Stop"

# Clear host and print a beautiful header
Clear-Host
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "                ZAMIL FULL-STACK PROJECT - LOCAL LAUNCHER             " -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Define paths
$RootPath = Get-Location
$BackendPath = Join-Path $RootPath "backendcode"
$VenvPath = Join-Path $BackendPath "venv"

# 1. Verify Python is installed
Write-Host "[*] Checking Python installation..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Gray
} catch {
    Write-Host "[!] Python is not installed or not in system PATH." -ForegroundColor Red
    Exit 1
}

# 2. Check virtual environment
Write-Host ""
Write-Host "[*] Checking Python Virtual Environment (venv)..." -ForegroundColor Blue
if (-not (Test-Path $VenvPath)) {
    Write-Host "  venv not found. Creating virtual environment in $VenvPath..." -ForegroundColor Yellow
    try {
        python -m venv $VenvPath
        Write-Host "  venv successfully created." -ForegroundColor Green
    } catch {
        Write-Host "[!] Failed to create venv." -ForegroundColor Red
        Exit 1
    }
} else {
    Write-Host "  venv found." -ForegroundColor Gray
}

# Activate venv & install dependencies
Write-Host ""
Write-Host "[*] Installing backend dependencies..." -ForegroundColor Blue
$PipPath = Join-Path $VenvPath "Scripts\pip.exe"
$PythonExe = Join-Path $VenvPath "Scripts\python.exe"

try {
    & $PipPath install --upgrade pip
    & $PipPath install -r (Join-Path $BackendPath "requirements.txt")
    Write-Host "  Dependencies installed successfully." -ForegroundColor Green
} catch {
    Write-Host "[!] Failed to install dependencies." -ForegroundColor Red
    Exit 1
}

# 3. Database migrations
Write-Host ""
Write-Host "[*] Running Django migrations..." -ForegroundColor Blue
$ManagePy = Join-Path $BackendPath "manage.py"
try {
    & $PythonExe $ManagePy migrate
    Write-Host "  Migrations applied." -ForegroundColor Green
} catch {
    Write-Host "[!] Migration failed." -ForegroundColor Red
    Exit 1
}

# 4. Ask to Seed Database if database is fresh
$DbPath = Join-Path $BackendPath "db.sqlite3"
$DbExists = Test-Path $DbPath
$SeedResponse = "N"

if (-not $DbExists) {
    Write-Host ""
    Write-Host "[?] SQLite database is fresh. Do you want to load seed data? (Y/N)" -ForegroundColor Yellow
    $SeedResponse = Read-Host
}

if ($SeedResponse -eq "Y" -or $SeedResponse -eq "y") {
    Write-Host "[*] Seeding default categories, specialities, status, and time templates..." -ForegroundColor Blue
    try {
        & $PythonExe $ManagePy loaddata (Join-Path $BackendPath "seed/categories.json")
        & $PythonExe $ManagePy loaddata (Join-Path $BackendPath "seed/specialities.json")
        & $PythonExe $ManagePy loaddata (Join-Path $BackendPath "seed/status.json")
        & $PythonExe $ManagePy loaddata (Join-Path $BackendPath "seed/time.json")
        Write-Host "  Database seeded successfully." -ForegroundColor Green
    } catch {
        Write-Host "  [!] Seed failed. Continuing..." -ForegroundColor Yellow
    }
}

# 5. Start Backend Server
Write-Host ""
Write-Host "[*] Launching Django backend server..." -ForegroundColor Blue

# We use Start-Process to launch Django in a separate cmd window so logs are visible but don't block this script
$DjangoCmdArgs = "/c title Zamil Django Backend && cd `"$BackendPath`" && `"$PythonExe`" manage.py runserver 0.0.0.0:8000"
Start-Process cmd.exe -ArgumentList $DjangoCmdArgs -WindowStyle Normal

# Wait 3 seconds to let Django boot
Start-Sleep -Seconds 3
Write-Host "  Django backend is starting on http://localhost:8000" -ForegroundColor Green

# 6. Check Flutter and Launch Front-End
Write-Host ""
Write-Host "[*] Checking Flutter Front-End..." -ForegroundColor Blue

try {
    $flutterVersion = flutter --version 2>&1
    Write-Host "  Found: Flutter SDK is ready." -ForegroundColor Gray
} catch {
    Write-Host "[!] Flutter SDK not found in system PATH. Cannot run frontend automatically." -ForegroundColor Red
    Write-Host "[!] Backend is running. You can run the Flutter app manually later." -ForegroundColor Yellow
    Exit 0
}

Write-Host ""
Write-Host "[?] Which device do you want to launch the Flutter frontend on?" -ForegroundColor Yellow
Write-Host "  1. Web (Chrome) - (Recommended for easy testing)" -ForegroundColor Gray
Write-Host "  2. Connected Device (Emulator/Physical Phone)" -ForegroundColor Gray
Write-Host "  3. Don't run frontend (Backend only)" -ForegroundColor Gray
$Choice = Read-Host -Prompt "Enter Choice (1-3)"

if ($Choice -eq "1") {
    Write-Host "[*] Starting Flutter app on Chrome web browser..." -ForegroundColor Green
    flutter run -d chrome
} elseif ($Choice -eq "2") {
    Write-Host "[*] Starting Flutter app on default connected device..." -ForegroundColor Green
    flutter run
} else {
    Write-Host "[*] Backend is running. Frontend was skipped." -ForegroundColor Yellow
}
