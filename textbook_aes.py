from aes.transformations import *
from aes.key_expansion import *

TEST = bytearray(range(16))


def dump_sboxes():
	# dump sboxes, as a test

	print("\nSBOX:")
	for a in range(16):
		row = ""
		for b in range(16):
			x = a*16+b
			row += "{:02x} ".format(sub_byte(x))
		print(row.strip())

	print("\niSBOX:")

	for a in range(16):
		row = ""
		for b in range(16):
			x = a*16+b
			row += "{:02x} ".format(inv_sub_byte(x))
		print(row.strip())


def key_expansion_test():
	ekey = key_expansion(TEST)
	for i in range(len(ekey)):
		print("{:02d}: {}".format(i, ekey[i].hex()))


def do_aes_128(_in, key):
	rkeys = key_expansion(key)
	state = add_round_key(_in, rkeys[0])

	for i in range(1, 10):
		state = sub_bytes(state)
		state = shift_rows(state)
		state = mix_columns(state)
		state = add_round_key(state, rkeys[i])

	state = sub_bytes(state)
	state = shift_rows(state)
	state = add_round_key(state, rkeys[-1])

	return state

#dump_sboxes()
#key_expansion_test()
for i in range(1000):
	do_aes_128(bytes.fromhex("00112233 44556677 8899aabb ccddeeff"), TEST)
print(do_aes_128(bytes.fromhex("00112233 44556677 8899aabb ccddeeff"), TEST).hex())

from Crypto.Cipher import AES
aes = AES.new(TEST, AES.MODE_ECB)
print(aes.encrypt(bytes.fromhex("00112233 44556677 8899aabb ccddeeff")).hex())
