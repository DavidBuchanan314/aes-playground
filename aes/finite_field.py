from .utils import bitn, blen

"""
	See section 4 of FIPS 197.
	
	Implements arithmetic over GF(2^8)
"""


#XXX: never actually used anywhere, here for reference
def ff_add(a, b):
	"""
		Section 4.1: Addition
		
		>>> hex(ff_add(0x57, 0x83))
		'0xd4'
		
	"""

	return a ^ b


def ff_divmod(a, b):
	"""
		Works like "long division"
		
		https://en.wikipedia.org/wiki/Finite_field_arithmetic#Rijndael.27s_finite_field
		
		        11111101111110 (mod) 100011011
		       ^100011011     
		       ---------------
		        01110000011110
		        ^100011011    
		        --------------
		         0110110101110
		         ^100011011   
		         -------------
		          010101110110
		          ^100011011  
		          ------------
		           00100011010
		            ^100011011
		            ----------
		             000000001
		
	"""

	q = 0
	r = a

	while blen(r) >= blen(b):
		q ^= 1 << (blen(r) - blen(b))
		r ^= b << (blen(r) - blen(b))

	return q, r


def ff_multiply(a, b, modulus=0x11b):
	"""
		Section 4.2: Multiplication
		
		>>> hex(ff_multiply(0x57, 0x83))
		'0xc1'
		
		>>> hex(ff_multiply(0x53, 0xca))
		'0x1'
		
	"""

	# polynomial product via "long multiplication"
	# similar to calculating 132*456 as:
	# 123*6 + 1230*5 + 12300*4
	result = 0
	for i in range(blen(b)):
		result ^= (a << i) * bitn(b, i)

	# calculate residue
	_, r = ff_divmod(result, modulus)

	return r


#def ff_multiplicative_inverse(n, modulus=0x11b, order=8):
#	for i in range(1, 1<<order):
#		if ff_multiply(n, i, modulus) == 1:
#			return i

def ff_multiplicative_inverse(a, modulus=0x11b):
	"""
		Based on extended Euclidean algorithm
		
		>>> hex(ff_multiplicative_inverse(0x53))
		'0xca'
		
	"""

	b = modulus
	x0, x1 = 0, 1
	while a:
		(q, a), b = ff_divmod(b, a), a
		x0, x1 = x1, x0 ^ ff_multiply(q, x1, modulus)

	return ff_divmod(x0, modulus)[1]
