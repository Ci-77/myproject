
import base64
import time
import hashlib
import hmac
import json
import traceback


SECRET_KEY = 'SECRET_KEY'
TOKEN_EXPIRE_TIME = 3600 

def generate_token(user_id):
    playload = {
        'user_id': user_id,
        'exp':int(time.time())+TOKEN_EXPIRE_TIME
    }
    playload_json = json.dumps(playload, separators=(',', ':'))
    playload_b64 = base64.urlsafe_b64encode(playload_json.encode('utf-8')).decode('utf-8')
    signature = hmac.new(SECRET_KEY.encode('utf-8'), playload_b64.encode('utf-8'), hashlib.sha256).hexdigest()
    token = '{}.{}'.format(playload_b64, signature)
    return token


def validate_token(auth_header):
    try:
        if auth_header.startswith('Bearer '):
            clientToken = auth_header[len('Bearer '):]  # 截取真正的token
        else:
            clientToken = auth_header 
        playload_b64, signature = clientToken.split('.')
        playload_json = base64.urlsafe_b64decode(playload_b64).decode('utf-8')
        playload = json.loads(playload_json)
        if playload['exp'] < int(time.time()):
            return 0
        signature_new = hmac.new(SECRET_KEY.encode('utf-8'), playload_b64.encode('utf-8'), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, signature_new):
            return 0
        return playload['user_id']
    except Exception as e:
        traceback.print_exc()
        return 0