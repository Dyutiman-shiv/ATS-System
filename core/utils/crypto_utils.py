import string, random
from hashlib import md5

def token_alphanum(size):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

def token_alphanum8():
    return token_alphanum(8)

def token_alphanum16():
    return token_alphanum(16)

def hq_hash(str):
    salt = 'HireQ:'
    str = salt + str
    return md5(str.encode("utf-8")).hexdigest()



