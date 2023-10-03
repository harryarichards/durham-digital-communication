try:
    import _pickle as pickle
except:
    import pickle
import sys
#Node class
class Node:
    #Each node requires a character and frequency, but can have a code and left and right children.
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.code = ''
        self.left = None
        self.right = None

def characterFrequencies(filestring):
    charFreqs = {}
    #For each character add it to a dictionary and each time the character appears increment its frequency by 1.
    for c in filestring:
        charFreqs[c] = charFreqs.get(c, 0) + 1
    #Sort the dictionary by frequency in descending order.
    charFreqs = sorted(charFreqs.items(), key=lambda x: x[1], reverse=True)
    #Return the dictionary.
    return (charFreqs)

def buildTree(treenodes):
    treenodes = list(treenodes)
    while len(treenodes) > 1:
        #Sort the nodes by frequency in descending order.
        treenodes.sort(key=lambda x: x.freq, reverse=True)
        #Set the children of the next node to be the nodes with least frequency.
        right, left = treenodes.pop(), treenodes.pop()
        #Create a node with frequency of the sum of its children, and set its children to the above 2 nodes.
        mergedNode = Node(None, left.freq + right.freq)
        mergedNode.right, mergedNode.left = right, left
        #Add the new nodes to the nodes list.
        treenodes.append(mergedNode)
        #If there's only one node in the list this is the root node, return it.
        if len(treenodes) == 1:
            return mergedNode


def formulateCodes(nodes):
    newNodes = []
    #For all of the nodes.
    for node in nodes:
        #If the node doesn't have a character.
        if (node.char is None):
            #Add 0 to the end of its left childs code.
            if node.left is not None:
                node.left.code = node.code + '0'
                newNodes.append(node.left)
            # Add 1 to the end of its left childs code.
            if node.right is not None:
                node.right.code = node.code + '1'
                newNodes.append(node.right)
            formulateCodes(newNodes)
        else:
            #If the nodes has a character, add the nodes character to a dictionary (as a key),
            #with the nodes code as its value - this represents a mapping.
            charCodes[node.char] = node.code

def encodeFile(filestring, map):
    newFileStringArray = []
    #For each character in the original string replace the character with its associated code.
    for i in filestring:
        newFileStringArray.append(map[i])
    newFileString = "".join(newFileStringArray)
    #Set the number of extra zeros required as the number of zeros the length of the string is away from the next
    #multiple of 8.
    extraZeros = 8 - len(newFileString)%8
    #Append this many zeros to the end of the new bit string.
    if extraZeros != 8:
        for i in range(extraZeros):
            newFileString += '0'
    b = bytearray()
    #For each 8 bits in the bit string convert these to an integer and append them to a byte array.
    for i in range(0, len(newFileString), 8):
        b.append(int(newFileString[i:i + 8], 2))
    return b, extraZeros

def writeEncodedFile(fileByteArray, dict, zeros):
    #Dump the byte array, dictionary and number of zeros to a file using pickle.
    with open(fname[:-4] + '.hc', 'wb') as compressedFile:
        pickle.dump(dict, compressedFile)
        pickle.dump(zeros, compressedFile)
        pickle.dump(fileByteArray, compressedFile)

if __name__ == '__main__':
    #Set the filename to the second argument in the command line
    fname = sys.argv[1]
    filestring = open(fname, 'r', newline='').read()
    #Make a dictionary of characters with their frequency, in descending frequency order.
    charFreqs = characterFrequencies(filestring)
    nodes = []
    #For each character in the dictionary make a node and add it to the nodes list.
    for char in charFreqs:
        node = Node(char[0], char[1])
        nodes.append(node)
    #Set root node to be the last node formed when building the tree.
    rootNode = buildTree(nodes)
    if rootNode != None:
        charCodes = {}
        formulateCodes([rootNode])
    #Special case for when their is only one character in the dicitonary, just set up a dictionary appropriately.
    else:
        charCodes = {filestring[0]: '0'}
    #Produce a byte string representing the original information,
    # and the the number of zeros needed to be added to the string to make it a multiple of 8.
    newFileString, extraZeros = encodeFile(filestring, charCodes)
    #Write the byte string, dictionary and number of zeros to a file.
    writeEncodedFile(newFileString, charCodes, extraZeros)