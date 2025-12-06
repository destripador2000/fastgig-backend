import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from config import settings

# Función para hashear (Convertir texto a hash seguro)
def hash_password(password: str) -> str:
    # 1. Convertimos el password (texto) a bytes, que es lo que pide la librería
    pwd_bytes = password.encode('utf-8')

    # 2. Generamos un "salt" (ruido aleatorio)
    salt = bcrypt.gensalt()

    # 3. Hasheamos
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)

    # 4. Devolvemos el hash como string para guardarlo en la BD
    return hashed_password.decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # 1. Copiamos los datos para no modificar el original
    to_encode = data.copy()

    # 2. Definimos cuándo caduca
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    # 3. Añadimos la fecha de expiración al diccionario
    to_encode.update({"exp": expire})

    # 4. Codificamos el JWT usando la Clave Secreta y el Algoritmo
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt