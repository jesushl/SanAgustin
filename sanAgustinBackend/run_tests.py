#!/usr/bin/env python3
"""
Script para ejecutar tests del proyecto San Agustín
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando: {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Función principal para ejecutar tests"""
    print("🏗️ San Agustín - Ejecutor de Tests")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not Path("main.py").exists():
        print("❌ Error: Debes ejecutar este script desde el directorio sanAgustinBackend/")
        sys.exit(1)
    
    # Verificar que pytest está instalado
    try:
        subprocess.run(["pytest", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: pytest no está instalado. Instálalo con: pip install pytest pytest-cov")
        sys.exit(1)
    
    # Ejecutar tests unitarios
    print("\n📋 Ejecutando tests unitarios...")
    unit_success = run_command(
        "pytest tests/unit/ -v --cov=services --cov-report=term-missing",
        "Tests Unitarios"
    )
    
    # Ejecutar tests de integración
    print("\n📋 Ejecutando tests de integración...")
    integration_success = run_command(
        "pytest tests/integration/ -v --cov=services.endpoints --cov-report=term-missing",
        "Tests de Integración"
    )
    
    # Ejecutar todos los tests
    print("\n📋 Ejecutando todos los tests...")
    all_tests_success = run_command(
        "pytest tests/ -v --cov=services --cov=repositories --cov=models --cov-report=term-missing --cov-report=html:htmlcov",
        "Todos los Tests"
    )
    
    # Generar reporte de cobertura
    print("\n📋 Generando reporte de cobertura...")
    coverage_success = run_command(
        "pytest tests/ --cov=services --cov=repositories --cov=models --cov-report=html:htmlcov --cov-report=xml",
        "Reporte de Cobertura"
    )
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE TESTS")
    print(f"{'='*60}")
    
    results = [
        ("Tests Unitarios", unit_success),
        ("Tests de Integración", integration_success),
        ("Todos los Tests", all_tests_success),
        ("Reporte de Cobertura", coverage_success)
    ]
    
    all_passed = True
    for test_type, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{test_type:<25} {status}")
        if not success:
            all_passed = False
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ¡Todos los tests pasaron exitosamente!")
        print("📁 Reporte de cobertura disponible en: htmlcov/index.html")
    else:
        print("⚠️ Algunos tests fallaron. Revisa los errores anteriores.")
    
    print(f"{'='*60}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
