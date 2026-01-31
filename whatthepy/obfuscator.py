import ast
import zlib
import base64
import random
import string
from . import key_store
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

fakes = [
    '''def {n}(d,k=None):
    if not d:return None
    r=[]
    for i,x in enumerate(d):
        r.append(x^k[i%len(k)] if k and i%2==0 else x)
    return bytes(r) if r else b""''',
    '''class {n}:
    _d={{}}
    def __init__(s,m='default'):s.m=m;s._b=bytearray()
    def write(s,c):s._b.extend(c);return len(c)
    def flush(s):o=bytes(s._b);s._b.clear();return o''',
    '''def {n}(s,e='utf-8'):return s.decode(e) if isinstance(s,bytes) else str(s)''',
    '''class {n}:
    def __init__(s,*a,**k):s._s={{}};s._l=False
    def acquire(s):s._l=True;return s
    def release(s):s._l=False
    def get(s,k):return s._s.get(k)''',
    '''def {n}(p,m='r'):
    with open(p,m) as f:return f.read()''',
    '''class {n}:
    def __enter__(s):return s
    def __exit__(s,*a):pass
    def process(s,d):return d''',
    '''def {n}(v,lo,hi):return max(lo,min(v,hi))''',
]

names = ['validate', 'decode', 'parse', 'transform', 'check', 'load',
         'read', 'cache', 'buffer', 'process', 'encode', 'serialize']

def name():
    return '_' + ''.join(random.choices('Il1O0', k=12))

def random_str(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def extract_imports(tree):
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imports.append(f"import {a.name}")
        elif isinstance(node, ast.ImportFrom):
            m = node.module or ''
            for a in node.names:
                imports.append(f"from {m} import {a.name}")
    return imports

def encrypt(data, key, nonce):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    enc = cipher.encryptor()
    return enc.update(data) + enc.finalize()

def scatter(encoded):
    chunks, i = [], 0
    while i < len(encoded):
        size = random.randint(15, 50)
        chunks.append(encoded[i:i+size])
        i += size
    return chunks

def make_decoys():
    return [base64.b85encode(bytes(random.randint(0, 255) for _ in range(random.randint(80, 200)))).decode('ascii')
            for _ in range(random.randint(2, 4))]

def make_vars(chunks, decoys):
    chunk_vars = [name() for _ in chunks]
    decoy_vars = [name() for _ in decoys]

    all_vars = [(v, c) for v, c in zip(chunk_vars, chunks)]
    all_vars += [(v, c) for v, c in zip(decoy_vars, decoys)]
    random.shuffle(all_vars)

    lines = [f"{v}='{c}'" for v, c in all_vars]

    for _ in range(random.randint(3, 6)):
        v = name()
        val = random.choice([f"'{random_str(random.randint(8,20))}'", f"{random.randint(100,9999)}"])
        lines.append(f"{v}={val}")

    random.shuffle(lines)
    return chunk_vars, lines

def batch_lines(lines):
    batched = []
    size = random.randint(4, 8)
    for i in range(0, len(lines), size):
        batched.append(';'.join(lines[i:i+size]))
    return batched

def make_decrypt_code(joined_var):
    dv, av, cv, cipv, decv, outv = name(), name(), name(), name(), name(), name()
    return [
        f"{dv}=__import__('base64').b85decode({joined_var})",
        f"{av}=__import__('cryptography.hazmat.primitives.ciphers',fromlist=['algorithms']).algorithms.AES",
        f"{cv}=__import__('cryptography.hazmat.primitives.ciphers',fromlist=['modes']).modes.CTR",
        f"{cipv}=__import__('cryptography.hazmat.primitives.ciphers',fromlist=['Cipher']).Cipher({av}(_key[:16]),{cv}(_key[16:]),__import__('cryptography.hazmat.backends',fromlist=['default_backend']).default_backend())",
        f"{decv}={cipv}.decryptor()",
        f"{outv}={decv}.update({dv})+{decv}.finalize()",
        f"exec(__import__('zlib').decompress({outv}).decode('utf-8'))",
    ]

def add_fake(lines):
    n = random.choice(names) + '_' + random_str(4)
    lines.append(random.choice(fakes).format(n=n))

def obfuscate(input_path, output_path, progress=None):
    def update(pct, msg):
        if progress:
            progress(pct, msg)

    update(0, "Reading...")
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()

    update(10, "Parsing...")
    tree = ast.parse(source)
    imports = extract_imports(tree)

    update(20, "Compressing...")
    data = zlib.compress(source.encode('utf-8'), 3)

    update(30, "Encrypting...")
    key = bytes(random.randint(0, 255) for _ in range(16))
    nonce = bytes(random.randint(0, 255) for _ in range(16))
    data = encrypt(data, key, nonce)

    update(40, "Making key...")
    kcode = key_store.make_key(key + nonce)

    update(50, "Encoding...")
    encoded = base64.b85encode(data).decode('ascii')

    update(60, "Scattering...")
    chunks = scatter(encoded)
    decoys = make_decoys()
    chunk_vars, var_lines = make_vars(chunks, decoys)

    update(70, "Building...")
    lines = [
        "try:from cryptography.hazmat.primitives.ciphers import Cipher as _C,algorithms as _A,modes as _M;from cryptography.hazmat.backends import default_backend as _B",
        "except:pass"
    ]

    if imports:
        size = random.randint(2, min(4, len(imports)))
        for i in range(0, len(imports), size):
            lines.append(';'.join(imports[i:i+size]))

    add_fake(lines)
    lines.extend(batch_lines(var_lines))

    ov, jv = name(), name()
    lines.append(f"{ov}=[{','.join(chunk_vars)}];{jv}=''.join({ov})")

    for line in key_store.make_loader(kcode).strip().split('\n'):
        if line:
            lines.append(line)

    lines.extend(make_decrypt_code(jv))
    add_fake(lines)

    update(90, "Writing...")
    output = '\n'.join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    update(100, "Done")

    return {
        'original_size': len(source),
        'final_size': len(output),
        'chunks': len(chunks),
        'decoys': len(decoys),
    }
