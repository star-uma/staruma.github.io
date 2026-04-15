#!/usr/bin/env powershell
<#
.SYNOPSIS
    Script para configurar y usar el entorno virtual de Python

.DESCRIPTION
    Este script automatiza la creación, activación y configuración del entorno virtual
    para el proyecto de exportación de autores a Excel.

.PARAMETER Action
    Acción a realizar: setup, activate, install, run, clean

.EXAMPLE
    .\setup_env.ps1 setup
    .\setup_env.ps1 run

.NOTES
    Autor: STAR UMA
    Fecha: Septiembre 2025
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("setup", "activate", "install", "run", "clean", "help")]
    [string]$Action
)

# Configuración
$VenvPath = ".venv"
$ScriptPath = "export_authors_to_excel.py"
$RequirementsPath = "requirements.txt"

function Show-Help {
    Write-Host "=== Gestor del Entorno Virtual Python ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\setup_env.ps1 <accion>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Acciones disponibles:" -ForegroundColor Green
    Write-Host "  setup     - Crear el entorno virtual e instalar dependencias" -ForegroundColor White
    Write-Host "  activate  - Mostrar comando para activar el entorno virtual" -ForegroundColor White
    Write-Host "  install   - Instalar/actualizar dependencias" -ForegroundColor White
    Write-Host "  run       - Ejecutar el script de exportación" -ForegroundColor White
    Write-Host "  clean     - Eliminar el entorno virtual" -ForegroundColor White
    Write-Host "  help      - Mostrar esta ayuda" -ForegroundColor White
    Write-Host ""
    Write-Host "Ejemplos:" -ForegroundColor Green
    Write-Host "  .\setup_env.ps1 setup" -ForegroundColor Gray
    Write-Host "  .\setup_env.ps1 run" -ForegroundColor Gray
}

function Setup-Environment {
    Write-Host "🚀 Configurando entorno virtual..." -ForegroundColor Cyan

    # Crear entorno virtual si no existe
    if (-not (Test-Path $VenvPath)) {
        Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
        python -m venv $VenvPath

        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Error al crear el entorno virtual" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "📦 Entorno virtual ya existe" -ForegroundColor Green
    }

    # Instalar dependencias
    Install-Dependencies

    Write-Host "✅ Entorno configurado correctamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para usar el entorno virtual:" -ForegroundColor Yellow
    Write-Host "  .\$VenvPath\Scripts\Activate.ps1" -ForegroundColor Gray
}

function Install-Dependencies {
    Write-Host "📋 Instalando dependencias..." -ForegroundColor Yellow

    if (-not (Test-Path $VenvPath)) {
        Write-Host "❌ Entorno virtual no encontrado. Ejecuta 'setup' primero." -ForegroundColor Red
        exit 1
    }

    # Activar entorno e instalar dependencias
    & ".\$VenvPath\Scripts\python.exe" -m pip install --upgrade pip
    & ".\$VenvPath\Scripts\python.exe" -m pip install -r $RequirementsPath

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencias instaladas correctamente!" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
        exit 1
    }
}


function Clean-Environment {
    Write-Host "🧹 Limpiando entorno virtual..." -ForegroundColor Yellow

    if (Test-Path $VenvPath) {
        Remove-Item -Recurse -Force $VenvPath
        Write-Host "✅ Entorno virtual eliminado" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  No hay entorno virtual que limpiar" -ForegroundColor Blue
    }
}

# Ejecutar acción
switch ($Action) {
    "setup" { Setup-Environment }
    "activate" { Show-Activate }
    "install" { Install-Dependencies }
    "run" { Run-Script }
    "clean" { Clean-Environment }
    "help" { Show-Help }
    default { Show-Help }
}
