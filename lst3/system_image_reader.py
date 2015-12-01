from __future__ import print_function
import struct
import array

with open("systemImage", 'rb') as f:
	symbols, = struct.unpack('i', f.read(4))
	print("symbols={}".format(symbols))
	count = 0
	while True:
		buffer = f.read(12)
		if not buffer:
			break
		index, cl, size = struct.unpack('iih', buffer[:10])
		read_size = size
		if (size < 0):
			size = ((-size) + 1) / 2;
		print("{:4d} {:4d} {:4d} {:4d} ".format(index << 1, cl, read_size, size), end='')
		#buffer = f.read(size * 4)
		if read_size > 0:
			data = array.array('i')
			data.fromfile(f, size)
			if read_size <= 16:
				for each in data[:16]:
					print("{:4} ".format(each), end='')
		if read_size < 0:
			string = f.read(size * 4)
			if cl == 8:
				print("\"{}\"".format(string[:-read_size-1]), end='')
		print("")
		count += 1
		#if count > 20:
		#	break
