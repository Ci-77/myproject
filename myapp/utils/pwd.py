

import hashlib


def generate_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password(password, hashed_password):  
    return generate_password(password) == hashed_password