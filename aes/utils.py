def bitn(i, n):
	return (i >> n) & 1


def blen(n):
	return n.bit_length()


def masknbits(n):
	return ((1<<n)-1)


def rotl(i, n, order=8):
	return ((i << n) | (i >> order-n)) & masknbits(order)
