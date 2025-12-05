import bcrypt

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
