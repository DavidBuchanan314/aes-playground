from .finite_field import ff_multiplicative_inverse
from .utils import rotl

# 5.1.1 SubBytes() Transformation
def sub_bytes(state):
	# apply sub_byte() to each element of the state
	return bytearray(map(sub_byte, state))


def inv_sub_bytes(state):
	# apply inv_sub_byte() to each element of the state
	return bytearray(map(inv_sub_byte, state))


def sub_byte(x):
	x = ff_multiplicative_inverse(x)

	# affine transform
	x ^= rotl(x, 1) ^ rotl(x, 2) ^ rotl(x, 3) ^ rotl(x, 4) ^ 0x63

	return x


def inv_sub_byte(x):
	# inverse affine transform
	x = rotl(x, 1) ^ rotl(x, 3) ^ rotl(x, 6) ^ 0x05

	return ff_multiplicative_inverse(x)
