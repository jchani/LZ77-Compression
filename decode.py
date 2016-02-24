import struct
import sys


def main():     
	MAX_SEARCH = int(sys.argv[1])
	fileType = sys.argv[2]
	
	outputFile = open("decompressed.%s" % (fileType), "wb")
	decodeFile("compressed.bin", outputFile, MAX_SEARCH)
	outputFile.close()

def decodeFile(filename, outputFile, MAX_SEARCH):
    f = open(filename,'rb')
    input = f.read()
    output = ""

    i = 0 
    while i < len(input):
    	#unpack string 3 bytes at a time
        (offset_and_length, char) = struct.unpack(">Hc", input[i:i+3]) 
        offset = offset_and_length >> 6 
        length = offset_and_length - (offset << 6)   
        # print("Offset: ", offset)
        # print("Length: ", length)
        i += 3
        
        #decode for no matches (0,0,char)
        if (offset == 0) and (length == 0): 
            output += char

        #decode when there is a match (offset, length, char)
        else:
            sPointer = len(output) - MAX_SEARCH
            if sPointer < 0: 
                sPointer = offset
            else: 
                sPointer += offset

            output += output[sPointer:sPointer+length] #add matched string
            output += char #add next char (after match)

    outputFile.write(output) 



if __name__ == '__main__':
	main()