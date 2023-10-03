try:
    import _pickle as pickle
except:
    import pickle
import sys

def decodeFile(maps, fileString):
    originalTextArray = []
    temp = ''
    #Add each character to the temp string one by one.
    for char in fileString:
        temp += char
        #If the temp string is a key.
        if temp in maps:
            #Append the associated value to an array.
            originalTextArray.append(str(maps[temp]))
            temp = ''
    #Return the value of the array joined together as a string.
    return "".join(originalTextArray)

if __name__ == '__main__':
    #Set filename equal to the second argument in the CL
    fname = sys.argv[1]
    #Open the compressed file, load the dictionary, number of zeros and bytearray.
    with open(fname, 'rb') as file:
        charFreqs = pickle.load(file)
        extraZeros = pickle.load(file)
        fileByteArray = pickle.load(file)
    #Invert the dictionary.
    charFreqs = {value: key for key, value in charFreqs.items()}
    fileStringArray = []
    #Parse each byte in the byte array so its the same form that it was encoded as.
    for originalByte in fileByteArray:
        byte = bin(originalByte)[2:].zfill(8)
        fileStringArray.append(byte)
    #Join the contents of the file string array to a string.
    binaryString = "".join(fileStringArray)
    #Remove the zeros that we padded the string with in encoding.
    if extraZeros != 8:
        binaryString = binaryString[:-extraZeros]
    originalText = decodeFile(charFreqs, binaryString)
    #Write the original text to a file.
    with open(fname[:-3]+ '.txt', 'w') as file:
        file.write(originalText)
