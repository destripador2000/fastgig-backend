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

# Función para verificar (Comparar texto plano contra hash guardado)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 1. Convertimos ambos a bytes
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')

    # 2. La librería se encarga de comparar de forma segura
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)