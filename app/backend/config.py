import os

# Configurazione per produzione
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
DATABASE_PATH = os.getenv("DATABASE_PATH", "synerchat.db")

# Configurazione JWT
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_DAYS = 7
