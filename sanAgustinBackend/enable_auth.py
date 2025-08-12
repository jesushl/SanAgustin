#!/usr/bin/env python3
"""
Script para habilitar la autenticación OAuth2.0 paso a paso
"""

import os
import sys

def enable_auth():
    """Habilita la autenticación descomentando las líneas necesarias"""
    
    main_py_path = "main.py"
    
    # Leer el archivo main.py
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Descomentar las importaciones de autenticación
    content = content.replace(
        "# from models.auth_models import Usuario, RegistroPendiente, Contacto as ContactoAuth",
        "from models.auth_models import Usuario, RegistroPendiente, Contacto as ContactoAuth"
    )
    
    # Descomentar las rutas de autenticación
    content = content.replace(
        "# from api.auth_routes import router as auth_router",
        "from api.auth_routes import router as auth_router"
    )
    content = content.replace(
        "# app.include_router(auth_router)",
        "app.include_router(auth_router)"
    )
    
    # Descomentar la configuración OAuth
    content = content.replace(
        "# from core.oauth_config import oauth",
        "from core.oauth_config import oauth"
    )
    content = content.replace(
        "# oauth.init_app(app)",
        "oauth.init_app(app)"
    )
    
    # Escribir el archivo actualizado
    with open(main_py_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Autenticación habilitada en main.py")

def disable_auth():
    """Deshabilita la autenticación comentando las líneas necesarias"""
    
    main_py_path = "main.py"
    
    # Leer el archivo main.py
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Comentar las importaciones de autenticación
    content = content.replace(
        "from models.auth_models import Usuario, RegistroPendiente, Contacto as ContactoAuth",
        "# from models.auth_models import Usuario, RegistroPendiente, Contacto as ContactoAuth"
    )
    
    # Comentar las rutas de autenticación
    content = content.replace(
        "from api.auth_routes import router as auth_router",
        "# from api.auth_routes import router as auth_router"
    )
    content = content.replace(
        "app.include_router(auth_router)",
        "# app.include_router(auth_router)"
    )
    
    # Comentar la configuración OAuth
    content = content.replace(
        "from core.oauth_config import oauth",
        "# from core.oauth_config import oauth"
    )
    content = content.replace(
        "oauth.init_app(app)",
        "# oauth.init_app(app)"
    )
    
    # Escribir el archivo actualizado
    with open(main_py_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Autenticación deshabilitada en main.py")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['enable', 'disable']:
        print("Uso: python enable_auth.py [enable|disable]")
        print("  enable  - Habilita la autenticación OAuth2.0")
        print("  disable - Deshabilita la autenticación OAuth2.0")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'enable':
        enable_auth()
    else:
        disable_auth()
