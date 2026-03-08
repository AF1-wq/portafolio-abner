# ============================================================================
# Script para iniciar servidor Flask - AbnerFranco.me + Wompi El Salvador
# EJECUTA TODO DE UNA - Backend + Frontend en UN PUERTO
# ============================================================================

Write-Host "`n" -ForegroundColor White
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🚀 INICIANDO SERVIDOR FLASK - ABNERFRANCO.ME + WOMPI        ║" -ForegroundColor Cyan
Write-Host "║       TODO INTEGRADO EN PUERTO 5000 - ¡DE UNA VEZ!           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n" -ForegroundColor White

# Detener cualquier proceso Node.js que pueda estar corriendo
Write-Host "🛑 Limpiando procesos antiguos..." -ForegroundColor Yellow
$nodeProc = Get-Process -Name node -ErrorAction SilentlyContinue
if ($nodeProc) {
    Stop-Process -Name node -Force -ErrorAction SilentlyContinue
    Write-Host "   [✓] Procesos Node.js detenidos" -ForegroundColor Green
} else {
    Write-Host "   [✓] No había procesos Node.js activos" -ForegroundColor Green
}

Write-Host "`n" -ForegroundColor White

# Verificar que Python está instalado
Write-Host "🔍 Verificando Python..." -ForegroundColor Yellow
$pythonVersion = py --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   [✓] Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   [❌] Python no está instalado o no está en PATH" -ForegroundColor Red
    exit 1
}

Write-Host "`n" -ForegroundColor White

# Verificar que .env existe
Write-Host "🔐 Verificando archivo .env..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   [✓] .env encontrado" -ForegroundColor Green
    $envContent = Get-Content .env | Select-String "WOMPI_APP_ID|MAIL_USERNAME" | Measure-Object | Select-Object -ExpandProperty Count
    if ($envContent -ge 2) {
        Write-Host "   [✓] Variables de entorno configuradas" -ForegroundColor Green
    } else {
        Write-Host "   [⚠] Algunas variables pueden estar faltando en .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "   [⚠] ADVERTENCIA: No se encontró .env - Los correos no funcionarán" -ForegroundColor Yellow
}

Write-Host "`n" -ForegroundColor White

# Verificar que flask está instalado
Write-Host "📦 Verificando dependencias..." -ForegroundColor Yellow
py -m pip show flask >$null 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   [✓] Flask está instalado" -ForegroundColor Green
} else {
    Write-Host "   [❌] Flask no está instalado. Instalando..." -ForegroundColor Yellow
    py -m pip install -r requirements.txt
}

Write-Host "`n" -ForegroundColor White

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✨ TODO LISTO - INICIANDO SERVIDOR..." -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "📍 En unos segundos aparecerá el servidor Flask" -ForegroundColor White
Write-Host "🌐 Acceso inmediato: http://localhost:5000" -ForegroundColor Green
Write-Host "⏹️  Para detener: Presiona Ctrl + C en esta terminal`n" -ForegroundColor White

# Iniciar Flask
py app.py
