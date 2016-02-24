import struct
import sys
import math

def LZ77_search(search, look_ahead):
	ls  = len(search)
	llh = len(look_ahead)
	buff = search + look_ahead

	if(ls == 0):
	#handle special case (same as no match found)
		return (0, 0, buff[0]) 

	if(llh == 0):
	#error condition, why would you call with empty look-ahead?
		return (-1,-1, "")

	best_offset = 0
	best_length = 0

	search_pointer = ls
	#print("search: %s,  lookahead: %s," % (search, look_ahead))
	for i in range(0,ls):
		#all of the potential starting positions for search
		offset = 0
		length = 0
		# print("The search pointer is: %d" % (search_pointer))
		while buff[i+length] == buff[search_pointer+length]:
			#found a match
			length += 1
			#check for search reaching the end of the look_ahead
			if search_pointer + length == len(buff):
				length -= 1
				break
			#check for offset+length reaching end of search_pointer
			if (i + length) == search_pointer:
				break

		if length > best_length:
			best_offset = i
			best_length = length

	return (best_offset, best_length, buff[search_pointer+best_length]) #Note: search_pointer+best_length is the index of the letter after

def main():
	fileName = sys.argv[1]
	MAX_SEARCH = int(sys.argv[2])
	MAX_LOOKAHEAD = int(math.pow(2, (math.log(65536, 2) - math.log(MAX_SEARCH, 2))))
	
	f = open(fileName, "rb")
	input = f.read()
	file = open("compressed.bin", "wb")
	search_idx = 0
	lookahead_idx = 0
	while lookahead_idx < len(input):
		search = input[search_idx:lookahead_idx]
		look_ahead = input[lookahead_idx:lookahead_idx+MAX_LOOKAHEAD]
		(offset, length, char) = LZ77_search(search, look_ahead)
		print(offset, length, char)

		
		shifted_offset = offset << 6
		offset_and_length = shifted_offset + length
		#pack into a 3-byte tuple for writing to a file
		packed_bytes = struct.pack(">Hc", offset_and_length, char)
		file.write(packed_bytes)

		lookahead_idx += length+1
		search_idx = lookahead_idx - MAX_SEARCH

		if(search_idx < 0):
			search_idx = 0

	file.close()



if __name__ == "__main__":
	main()





