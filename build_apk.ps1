# Zamil Flutter APK Builder
# This script compiles the Flutter application into a release APK.

$ErrorActionPreference = "Stop"

Clear-Host
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "                ZAMIL FLUTTER APP - RELEASE BUILDER                   " -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verify Flutter SDK is installed
Write-Host "[*] Checking Flutter SDK..." -ForegroundColor Blue
try {
    $flutterVersion = flutter --version 2>&1
} catch {
    Write-Host "[!] Flutter SDK is not installed or not in system PATH." -ForegroundColor Red
    Exit 1
}

# 2. Get API Base URL
Write-Host ""
Write-Host "[?] Enter the Production Backend API URL (e.g., https://your-domain.com/api/):" -ForegroundColor Yellow
Write-Host "    (Press ENTER to use default development server http://10.245.142.235:8000/api/)" -ForegroundColor Gray
$ApiUrl = Read-Host

# 3. Clean project
Write-Host ""
Write-Host "[*] Cleaning old build files..." -ForegroundColor Blue
try {
    flutter clean
    Write-Host "  Flutter project cleaned." -ForegroundColor Green
} catch {
    Write-Host "[!] Failed to clean flutter build cache. Continuing..." -ForegroundColor Yellow
}

# 4. Get Packages
Write-Host ""
Write-Host "[*] Fetching dependencies..." -ForegroundColor Blue
try {
    flutter pub get
    Write-Host "  Dependencies updated." -ForegroundColor Green
} catch {
    Write-Host "[!] Failed to fetch packages." -ForegroundColor Red
    Exit 1
}

# 5. Build APK
Write-Host ""
Write-Host "[*] Compiling Release APK..." -ForegroundColor Blue
try {
    if ($ApiUrl.Trim() -ne "") {
        Write-Host "  Building with custom API Base URL: $ApiUrl" -ForegroundColor Gray
        flutter build apk --release --dart-define=API_BASE_URL=$ApiUrl
    } else {
        Write-Host "  Building with default API Base URL..." -ForegroundColor Gray
        flutter build apk --release
    }
    Write-Host "  Compilation completed successfully." -ForegroundColor Green
} catch {
    Write-Host "[!] Flutter compilation failed." -ForegroundColor Red
    Exit 1
}

# 6. Organize Output
Write-Host ""
Write-Host "[*] Packaging release artifacts..." -ForegroundColor Blue

$RootDir = Get-Location
$DistDir = Join-Path $RootDir "dist"
$SourceApk = Join-Path $RootDir "build\app\outputs\flutter-apk\app-release.apk"
$TargetApk = Join-Path $DistDir "zamil-app-release.apk"

if (-not (Test-Path $DistDir)) {
    New-Item -ItemType Directory -Path $DistDir | Out-Null
}

if (Test-Path $SourceApk) {
    Copy-Item -Path $SourceApk -Destination $TargetApk -Force
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host " SUCCESS: Release APK has been built and organized!" -ForegroundColor Green
    Write-Host " Location: $TargetApk" -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Green
} else {
    Write-Host "[!] Built APK could not be located in output directory." -ForegroundColor Red
}
