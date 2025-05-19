import jwt
import datetime
import secrets

def obter_secret_key():
    # Gerar uma chave secreta automaticamente
    return secrets.token_hex(32)

def gerar_token(usuario_id):
    payload = {
        'id_usuario': usuario_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira em 1 hora
    }
    secret_key = obter_secret_key()
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verificar_token(token):
    try:
        secret_key = obter_secret_key()
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado.")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido.")
