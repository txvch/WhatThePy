import random
import zlib
import base64

def name():
    return '_' + ''.join(random.choices('Il1O0', k=12))

def fmt(lst):
    return '[' + ','.join(str(x) for x in lst) + ']'

def chunk(data):
    return [list(data[i:i+2]) for i in range(0, len(data), 2)]

def make_key(key):
    if not key or len(key) < 8:
        raise ValueError("key too short")

    key = bytes(key)
    n = len(key)

    m1 = bytes(random.randint(0, 255) for _ in range(n))
    m2 = bytes(random.randint(0, 255) for _ in range(n))
    m3 = bytes(random.randint(0, 255) for _ in range(n))

    idx = list(range(n))
    random.shuffle(idx)
    rev = [0] * n
    for i, x in enumerate(idx):
        rev[x] = i

    shuffled = bytes(key[i] for i in idx)
    masked = bytes((shuffled[i] ^ m1[i] ^ m2[i] ^ m3[i]) for i in range(n))

    mc, m1c, m2c, m3c, ic = chunk(masked), chunk(m1), chunk(m2), chunk(m3), chunk(rev)

    decoys = [[random.randint(0, 255) for _ in range(random.randint(1, 3))]
              for _ in range(random.randint(10, 18))]

    mv = [name() for _ in mc]
    m1v = [name() for _ in m1c]
    m2v = [name() for _ in m2c]
    m3v = [name() for _ in m3c]
    iv = [name() for _ in ic]
    dv = [name() for _ in decoys]

    assigns = []
    for v, c in zip(mv, mc): assigns.append(f"{v}={fmt(c)}")
    for v, c in zip(m1v, m1c): assigns.append(f"{v}={fmt(c)}")
    for v, c in zip(m2v, m2c): assigns.append(f"{v}={fmt(c)}")
    for v, c in zip(m3v, m3c): assigns.append(f"{v}={fmt(c)}")
    for v, c in zip(iv, ic): assigns.append(f"{v}={fmt(c)}")
    for v, c in zip(dv, decoys): assigns.append(f"{v}={fmt(c)}")
    random.shuffle(assigns)

    vm, v1, v2, v3, vi = name(), name(), name(), name(), name()
    f1, f2, f3 = name(), name(), name()

    code = assigns + [
        f"{vm}=[_x for _s in [{','.join(mv)}] for _x in _s]",
        f"{v1}=[_x for _s in [{','.join(m1v)}] for _x in _s]",
        f"{v2}=[_x for _s in [{','.join(m2v)}] for _x in _s]",
        f"{v3}=[_x for _s in [{','.join(m3v)}] for _x in _s]",
        f"{vi}=[_x for _s in [{','.join(iv)}] for _x in _s]",
        f"{f1}=lambda _d,_a,_b,_c:[_d[_i]^_a[_i]^_b[_i]^_c[_i] for _i in range(len(_d))]",
        f"{f2}=lambda _d,_p:[_d[_p[_i]] for _i in range(len(_d))]",
        f"{f3}=lambda:{f2}({f1}({vm},{v1},{v2},{v3}),{vi})",
        f"def get():return bytes({f3}())",
    ]

    return '\n'.join(code)

def make_loader(code):
    compressed = zlib.compress(code.encode('utf-8'), 9)
    encoded = base64.b85encode(compressed).decode('ascii')

    size = random.randint(35, 55)
    chunks = [encoded[i:i+size] for i in range(0, len(encoded), size)]
    vars = [name() for _ in chunks]

    parts = [f"{v}='{c}'" for v, c in zip(vars, chunks)]

    jv, ns = name(), name()
    parts.extend([
        f"{jv}=''.join([{','.join(vars)}])",
        f"{ns}={{}}",
        f"exec(__import__('zlib').decompress(__import__('base64').b85decode({jv})).decode(),{ns})",
        f"_key={ns}['get']()",
    ])

    return '\n'.join(parts)
