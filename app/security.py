import os
import bcrypt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"

def hash_senha(senha: str):
    # O bcrypt precisa de bytes. Limitamos a 72 bytes para evitar o erro.
    senha_bytes = senha.encode('utf-8')[:72]
    return bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')

def verificar_senha(senha_plana: str, senha_hash: str):
    senha_bytes = senha_plana.encode('utf-8')[:72]
    hash_bytes = senha_hash.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_bytes)

def criar_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None