from aes.transformations import *
from aes.key_expansion import *


"""
See "A Tutorial on White-box AES", section 3.2
"""

TESTKEY = bytearray(range(16))
TESTDAT = bytes.fromhex("00112233 44556677 8899aabb ccddeeff")

RKEYS = key_expansion(TESTKEY)
RKEYSs = [shift_rows(rkey) for rkey in RKEYS[:-1]] + RKEYS[-1:]  # dont' shift the last round

SBOX = [sub_byte(x) for x in range(0x100)]

TBOX = [[[SBOX[i ^ RKEYSs[r][ki]] for i in range(0x100)] for ki in range(16)] for r in range(10)]


def do_aes_128(_in, key):
	s = _in

	for t in TBOX[:9]:
		s = [t[0x0][s[0x0]], t[0x1][s[0x5]], t[0x2][s[0xa]], t[0x3][s[0xf]],
		     t[0x4][s[0x4]], t[0x5][s[0x9]], t[0x6][s[0xe]], t[0x7][s[0x3]],
		     t[0x8][s[0x8]], t[0x9][s[0xd]], t[0xa][s[0x2]], t[0xb][s[0x7]],
		     t[0xc][s[0xc]], t[0xd][s[0x1]], t[0xe][s[0x6]], t[0xf][s[0xb]]]
		s = mix_columns(s)

	t = TBOX[-1]
	s = [t[0x0][s[0x0]], t[0x1][s[0x5]], t[0x2][s[0xa]], t[0x3][s[0xf]],
	     t[0x4][s[0x4]], t[0x5][s[0x9]], t[0x6][s[0xe]], t[0x7][s[0x3]],
	     t[0x8][s[0x8]], t[0x9][s[0xd]], t[0xa][s[0x2]], t[0xb][s[0x7]],
	     t[0xc][s[0xc]], t[0xd][s[0x1]], t[0xe][s[0x6]], t[0xf][s[0xb]]]

	s = add_round_key(s, RKEYS[-1])

	return s


print(do_aes_128(TESTDAT, TESTKEY).hex())

from Crypto.Cipher import AES
print(AES.new(TESTKEY, AES.MODE_ECB).encrypt(TESTDAT).hex())
