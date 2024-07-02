import hashlib
def md5(data):
    return hashlib.md5(data).digest()

def sha512(data):
    return hashlib.sha512(data).digest()

def xor_bytes(b1, b2):
    return bytes(x ^ y for x, y in zip(b1, b2))

def pad_key(key, block_size):
    if len(key) > block_size:
        key = hashlib.md5(key.encode()).digest()
    return key.ljust(block_size, b'\x00')

def hmac(key, data, hash_func):
    if hash_func == 'MD5':
        inner_hash_func = md5
        block_size = 64
    elif hash_func == 'SHA512':
        inner_hash_func = sha512
        block_size = 128
    else:
        raise ValueError("Unsupported hash function")
    
    padded_key = pad_key(key.encode(), block_size)
    ipad = xor_bytes(padded_key, b'\x36' * block_size)
    opad = xor_bytes(padded_key, b'\x5c' * block_size)

    inner_hash = inner_hash_func(ipad + data.encode())
    outer_hash = hashlib.md5(opad + inner_hash).hexdigest()

    return outer_hash


key = "Jefe"
data = "Hi There"
print("MD5:", hmac(key, data, 'MD5'))
print("SHA512:", hmac(key, data, 'SHA512'))
