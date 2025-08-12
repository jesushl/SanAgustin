from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi import Request
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración OAuth
config = Config('.env')
oauth = OAuth()

# Configuración Google OAuth
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID', 'your_google_client_id'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET', 'your_google_client_secret'),
    server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Configuración Facebook OAuth
oauth.register(
    name='facebook',
    client_id=os.getenv('FACEBOOK_CLIENT_ID', 'your_facebook_client_id'),
    client_secret=os.getenv('FACEBOOK_CLIENT_SECRET', 'your_facebook_client_secret'),
    api_base_url='https://graph.facebook.com/',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    client_kwargs={
        'scope': 'email public_profile'
    }
)

# URLs de redirección
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/callback"
FACEBOOK_REDIRECT_URI = "http://localhost:8000/auth/facebook/callback"

# Configuración JWT
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here_change_in_production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
