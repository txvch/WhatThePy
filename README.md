<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/platform-windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

<p align="center">
  <img src="assets/banner.png" alt="WhatThePy" width="600">
</p>

<h3 align="center">
  <sub>People kept telling me my code looked bad. So I wrote a tool to make it worse (on purpose)</sub>
</h3>

---

## What Is This?

**WhatThePy** obfuscates Python code using AES-128-CTR encryption, triple XOR key masking, byte permutation, and compression. The result is compact, messy code that still runs fine.

**Important:** This is for fun and learning. It deters casual viewers but won't stop determined attackers.

---

## Before & After

<table>
<tr>
<th>Your Code</th>
<th>After WhatThePy</th>
</tr>
<tr>
<td>

```python
def greet(name):
    message = f"Hello, {name}!"
    print(message)
    return message

if __name__ == "__main__":
    greet("World")
```

</td>
<td>

```python
try:from cryptography.hazmat.primitives.ciphers import Cipher as _C,algorithms as _A,modes as _M;from cryptography.hazmat.backends import default_backend as _B
except:pass
class load_AMWW:
    _d={}
    def __init__(s,m='default'):s.m=m;s._b=bytearray()
    def write(s,c):s._b.extend(c);return len(c)
    def flush(s):o=bytes(s._b);s._b.clear();return o
_I111lO0OlOOl='R)8&iF4sw|%+}~N=)dV^nk>Gi...';_II1I00OO0O0O='Y!BDc9le|LelyiQgy`>t';_OO1O1Ol1IOOI=2454
_l1OI1OIO00Il=[_l11lIl011l10,_1O0llO101III,...];_OI10lIIOlI11=''.join(_l1OI1OIO00Il)
_10II1I101IO1=''.join([_1O01I0IlOO1O,_IIO0I00OlIOI,...])
_IO1OOI111lII={}
exec(__import__('zlib').decompress(__import__('base64').b85decode(_10II1I101IO1)).decode(),_IO1OOI111lII)
_key=_IO1OOI111lII['get']()
_IOlIOO0lOl1l=__import__('base64').b85decode(_OI10lIIOlI11)
_1O101IOOIl10=__import__('cryptography.hazmat.primitives.ciphers',fromlist=['algorithms']).algorithms.AES
_00lIO00llO11=__import__('cryptography.hazmat.primitives.ciphers',fromlist=['modes']).modes.CTR
_lll10I0I0OIl=__import__('cryptography.hazmat.primitives.ciphers',fromlist=['Cipher']).Cipher(_1O101IOOIl10(_key[:16]),_00lIO00llO11(_key[16:]),__import__('cryptography.hazmat.backends',fromlist=['default_backend']).default_backend())
_lllIIIO0l00l=_lll10I0I0OIl.decryptor()
_O1O0O1O0I0I1=_lllIIIO0l00l.update(_IOlIOO0lOl1l)+_lllIIIO0l00l.finalize()
exec(__import__('zlib').decompress(_O1O0O1O0I0I1).decode('utf-8'))
```

</td>
</tr>
</table>

---

## Installation

```bash
git clone https://github.com/txvch/WhatThePy.git
cd WhatThePy
pip install -r requirements.txt
```

**Requirements:** Python 3.8+, `rich`, `pyfiglet`, `cryptography`

---

## Usage

```bash
python -m whatthepy
# Enter your file path when prompted
# Output: yourfile_obfuscated.py
```

Works with PyInstaller:
```bash
pyinstaller --onefile yourfile_obfuscated.py
```

---

## Protection Level

| Threat | Protected? |
|--------|-----------|
| Script kiddies | Yes |
| Casual copy-paste | Yes |
| Quick glances | Yes |
| Basic static analysis | Partially |
| Motivated attackers | Slows them down |
| Good reverse engineers | No |

**Good for:** Learning, CTF challenges, deterring casual viewers
**Not for:** Protecting secrets, valuable IP, or anything critical

---

## How It Works

```
Source Code
    |
    v
[1] Compress (zlib)
    |
    v
[2] Encrypt (AES-128-CTR)
    |
    v
[3] Encode (Base85)
    |
    v
[4] Scatter into chunks with decoys
    |
    v
[5] Key Protection:
    - Triple XOR masking
    - Byte permutation shuffle
    - Split into 2-byte chunks
    - Mixed with 10-18 decoy variables
    - Compressed & encoded
    |
    v
Obfuscated Output
```

---

## Disclaimer

This is a fun project for learning and experimentation. It makes code harder to casually read but doesn't provide serious protection. Use it for fun, learning, or light deterrence - not for anything critical.

Made this as a weekend project and please.. Don't use it for serious security needs!

---

## License

MIT License - Do whatever you want with it, just don't blame me!

---

<p align="center">
  <sub>Made with questionable decisions and too much redbull😭</sub>
</p>
