from aes.finite_field import *

from aes.sub_bytes import *

# dump sboxes, as a test

for a in range(16):
	row = ""
	for b in range(16):
		x = a*16+b
		row += "{:02x} ".format(sub_byte(x))
	print(row.strip())

print()

for a in range(16):
	row = ""
	for b in range(16):
		x = a*16+b
		row += "{:02x} ".format(inv_sub_byte(x))
	print(row.strip())
