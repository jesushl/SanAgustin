#!/usr/bin/env python3
"""
Script para probar la nueva arquitectura separada del proyecto San Agustín
"""

import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todos los módulos se pueden importar correctamente"""
    print("🧪 Probando imports de la nueva arquitectura...")
    
    try:
        # Probar imports de modelos
        from models.database import Base, Departamento, AreaComun, LugarVisita, Estacionamiento, ReservaAreaComun, ReservaVisita, Adeudo
        print("✅ Modelos de base de datos importados correctamente")
        
        from models.schemas import DepartamentoResponse, EstacionamientoResponse, AreaComunResponse, LugarVisitaResponse
        print("✅ Esquemas Pydantic importados correctamente")
        
        # Probar imports de repositorios
        from repositories import BaseRepository, DepartamentoRepository, EstacionamientoRepository, AreaComunRepository
        print("✅ Repositorios importados correctamente")
        
        # Probar imports de servicios
        from services import PanelResidenteService, EstacionamientoService, AreaComunService, LugarVisitaService
        print("✅ Servicios importados correctamente")
        
        # Probar imports de endpoints
        from services.endpoints import panel_residente_router, estacionamiento_router, area_comun_router
        print("✅ Endpoints importados correctamente")
        
        # Probar imports de configuración
        from core.database import get_db, engine
        from core.auth import get_current_user
        print("✅ Configuración central importada correctamente")
        
        print("\n🎉 ¡Todas las importaciones funcionan correctamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("\n🗄️ Probando conexión a la base de datos...")
    
    try:
        from core.database import engine
        from models.database import Base
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos configurada correctamente")
        
        # Probar conexión
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Conexión a la base de datos exitosa")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de base de datos: {e}")
        return False

def test_service_instantiation():
    """Prueba la instanciación de servicios"""
    print("\n🔧 Probando instanciación de servicios...")
    
    try:
        from services import PanelResidenteService, EstacionamientoService, AreaComunService, LugarVisitaService
        
        # Instanciar servicios
        panel_service = PanelResidenteService()
        estacionamiento_service = EstacionamientoService()
        area_comun_service = AreaComunService()
        lugar_visita_service = LugarVisitaService()
        
        print("✅ Todos los servicios se instanciaron correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al instanciar servicios: {e}")
        return False

def test_repository_instantiation():
    """Prueba la instanciación de repositorios"""
    print("\n📚 Probando instanciación de repositorios...")
    
    try:
        from repositories import DepartamentoRepository, EstacionamientoRepository, AreaComunRepository, LugarVisitaRepository
        
        # Instanciar repositorios
        depto_repo = DepartamentoRepository()
        est_repo = EstacionamientoRepository()
        area_repo = AreaComunRepository()
        lugar_repo = LugarVisitaRepository()
        
        print("✅ Todos los repositorios se instanciaron correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al instanciar repositorios: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🏗️ San Agustín - Pruebas de Arquitectura Separada")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database_connection,
        test_service_instantiation,
        test_repository_instantiation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("📊 Resumen de Pruebas")
    print("=" * 30)
    print(f"✅ Pruebas pasadas: {passed}/{total}")
    print(f"❌ Pruebas fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! La arquitectura está funcionando correctamente.")
        return 0
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revisa los errores anteriores.")
        return 1

if __name__ == "__main__":
    exit(main())
