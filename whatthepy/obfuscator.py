import ast
import zlib
import base64
import random
import string

fake_funcs = [
    '''def {name}(data, key=None):
    if not data:
        return None
    result = []
    for i, x in enumerate(data):
        if key and i % 2 == 0:
            result.append(x ^ key[i % len(key)])
        else:
            result.append(x)
    return bytes(result) if result else b""''',

    '''def {name}(config):
    cache = {{}}
    def inner(k, v=None):
        if v is None:
            return cache.get(k)
        cache[k] = v
        return v
    for k, v in config.items():
        inner(k, v)
    return inner''',

    '''class {name}:
    _data = {{}}
    def __init__(self, mode='default'):
        self.mode = mode
        self._buf = bytearray()
    def write(self, chunk):
        self._buf.extend(chunk)
        return len(chunk)
    def flush(self):
        out = bytes(self._buf)
        self._buf.clear()
        return out''',
]

fake_names = ['validate', 'decode', 'parse', 'transform', 'check', 'load', 'read', 'cache', 'buffer', 'stream']

def scramble():
    return '_' + ''.join(random.choices('Il1O0', k=12))

def random_str(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def xor(data, key):
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ key[i % len(key)]
    return bytes(out)

def obfuscate(input_path, output_path, progress=None):
    def update(pct, msg):
        if progress:
            progress(pct, msg)

    update(0, "Reading file...")
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()

    update(10, "Checking syntax...")
    ast.parse(source)

    update(20, "Encoding source...")
    data = source.encode('utf-8')

    update(30, "Compressing...")
    data = zlib.compress(data, 3)

    update(40, "Encrypting...")
    key = bytes(random.randint(0, 255) for _ in range(16))
    data = xor(data, key)

    update(50, "Encoding...")
    encoded = base64.b85encode(data).decode('ascii')

    update(60, "Scattering...")

    chunks = []
    i = 0
    while i < len(encoded):
        size = random.randint(15, 50)
        chunks.append(encoded[i:i+size])
        i += size

    chunk_vars = [scramble() for _ in chunks]

    decoy_count = random.randint(2, 4)
    decoys = []
    decoy_vars = []
    for _ in range(decoy_count):
        fake = bytes(random.randint(0, 255) for _ in range(random.randint(80, 200)))
        decoys.append(base64.b85encode(fake).decode('ascii'))
        decoy_vars.append(scramble())

    update(80, "Building output...")

    lines = []
    lines.append("import sys, os")
    lines.append("from typing import Optional, Any")
    lines.append("")

    name = random.choice(fake_names) + '_' + random_str(4)
    lines.append(random.choice(fake_funcs).format(name=name))
    lines.append("")

    all_vars = []
    for var, chunk in zip(chunk_vars, chunks):
        all_vars.append((var, chunk, True))
    for var, chunk in zip(decoy_vars, decoys):
        all_vars.append((var, chunk, False))

    random.shuffle(all_vars)

    for var, chunk, _ in all_vars:
        lines.append(f"{var} = '{chunk}'")

    lines.append("")
    name = random.choice(fake_names) + '_' + random_str(4)
    lines.append(random.choice(fake_funcs).format(name=name))
    lines.append("")

    order_var = scramble()
    lines.append(f"{order_var} = [{', '.join(chunk_vars)}]")

    key_var = scramble()
    lines.append(f"{key_var} = {key}")

    joined_var = scramble()
    lines.append(f"{joined_var} = ''.join({order_var})")

    lines.append("")

    lines.append(f"exec(__import__('zlib').decompress((lambda d,k:bytes(a^b for a,b in zip(d,__import__('itertools').cycle(k))))(__import__('base64').b85decode({joined_var}),{key_var})).decode('utf-8'))")

    lines.append("")

    name = random.choice(fake_names) + '_' + random_str(4)
    lines.append(random.choice(fake_funcs).format(name=name))
    lines.append("")

    update(90, "Writing...")
    output = '\n'.join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    update(100, "Done")

    return {
        'original_size': len(source),
        'final_size': len(output),
        'chunks': len(chunks),
        'decoys': decoy_count,
    }
