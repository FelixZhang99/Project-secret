# Compression and Encryption
# 
# This is a program that can compress and encrypt text.
# It uses Huffman coding to compress the text, store it
# and the map in a binary string,
# then translate it into numbers. 


# The output of encryption will be in binary form, therefore,
# we need a tree to store the information.
# This is a node that store left, right, value and the letter
class node:

    # Initial with left and right node,
    # the value and letter for this node if present 
    def __init__(self, left = None, right = None, value = 0, letter = None):
        self.left = left
        self.right = right
        self.value = value
        self.letter = letter
        
    # This is needed for calling sort method
    def __lt__(self, other):
        return self.value < other.value



# We need to translate text into dictionary first 
# We use dictionary so that we don't need to loop through
# the container to get the key we want
def translate(text):
    
    # First make an empty dictionary with only EOF,
    # which represent the end of the file
    output = {}
    output.update({"EOF": 1})
    
    # Loop through each char in the text
    for char in text:
        
        # If char is in dictionary, add one for the value of it
        if char in output:
            value = output.get(char) + 1
            output.update({char: value})
            
        # Otherwise, create a new key
        else:
            output.update({char: 1})
    
    # Output the dictionary
    return output



# Create a list of nodes for the map
def createNode(my_map):
    
    # First initate an empty list
    my_output = []
    
    # Create a new node and
    for item in my_map.items():
        newNode = node(None, None, item[1], item[0])
        my_output.append(newNode)
        
    # Sort the list for later use
    my_output.sort(reverse = True)
    return my_output



# Create a tree with large value on the top part and small value on lower part 
def getTree(q):
    
    # Get the first two value in the list, which has the smallest value,
    # Create a new node with these two nodes as subnodes,
    # Reinsert the node into the list and sort it to make first two smallest value
    # in the front again
    while len(q) > 1:
        left = q.pop()
        right = q.pop()
        newValue = left.value + right.value
        newNode = node(left, right, newValue, None)
        q.append(newNode)
        q.sort(reverse = True)
        
    # Pop the only node left, which is the parent node
    return q.pop()



# Now we make the tree into a dictionary with recursion
def getDictionary(my_node, currentStr, dictionary):
    
    # Base case, if reach the end of the tree, which has letter in it,
    # add it into dictionary and return
    if my_node.letter != None:
        dictionary.update({my_node.letter: currentStr})
        return dictionary
    
    # Recursion case, go left and add 0 to the string,
    # go right and add 1 to the string, and return the result
    else:
        dictionary = getDictionary(my_node.left, currentStr + '0', dictionary)
        dictionary = getDictionary(my_node.right, currentStr + '1', dictionary)
        return dictionary



# Translate the text into 0 and 1s
def makeStr(text, dictionary):
    output = ""
    
    # Go through all the char in the text, use the dictionary to translate
    # every char into a string of 0s and 1s
    for char in text:
        output += dictionary.get(char)
        
    # At the end, add EOF to the output
    output += dictionary.get("EOF")
    return output



# Translate the binary into unicode
def makeHex(string):
    hexstr = ""
    output = ""
    
    # This loop through the binary, cut every 7 chars
    # and make them into a new char with bigger unicorn value
    # Thus the total amount of memory need to store it is reduced
    for char in string:
        hexstr += char
        if len(hexstr) == 7:
            output += makeChar(hexstr)
            hexstr = ""
            
    # For the last one, fill it with 0s at the end and find the char
    output += makeChar(hexstr + '0' * (7 - len(hexstr)))
    return output



# This function turns a string of 0 and 1 into an unicorn character
def makeChar(string):
    index = 1
    number = 0
    
    # Go through the string, if find a '1',
    # add the recult with the value associated with the index
    for char in string[::-1]:
        if char == "1":
            number += index
        index *= 2
    
    # Output the unicorn value of the number
    return chr(number)



# Compress and encrypt the text
def compress(text):
    
    # Call all the functions we defined and return the compressed
    # and encrpted text and the key dictionary for the text
    my_dict = translate(text)
    q = createNode(my_dict)
    my_node = getTree(q)
    bi_dict = getDictionary(my_node, "", {})
    binary = makeStr(text, bi_dict)
    unicode = makeHex(binary)
    return (unicode, bi_dict)



# When depress, first make the map
def makeMap(my_dict):
    
    # Create the parent node with no value in it
    parent_node = node()
    
    # For each key in the dictionary, create a path to it
    for item in my_dict.keys():
        code = my_dict.get(item)
        current = parent_node
        
        # For each char in the path, if it is a '0', go left,
        # otherwise go right,
        # Create new node if the node doesnt exist
        for char in code:
            if char == '0':
                if current.left == None:
                    current.left = node()
                current = current.left
            else:
                if current.right == None:
                    current.right = node()
                current = current.right
        current.letter = item
    return parent_node



# Translate the string into binary
def makeBinary(string):
    output = ""
    
    # For each char in the string, translate it into binary
    for char in string:
        this_char = ""
        number = ord(char)
        
        # For each value in the binary, if it is bigger than that value,
        # minus it and place a '1' in that position
        # If it is smaller, place a '0' in that position
        for i in range(7)[::-1]:
            if number >= 2 ** i:
                this_char += "1"
                number -= 2 ** i
            else:
                this_char += "0"
        output += this_char
    return output



# Read from the string to get the original text
def makeText(string, parent):
    current = parent
    output = ""
    
    # For each char in the string, if it is zero,
    # go left, if it is one, go right, until find a letter
    # put that letter in and go back to parent to repeat the steps,
    # until find a EOF char
    for char in string:
        if char == '0':
            current = current.left
        else:
            current = current.right
        if current.letter != None:
            if current.letter == "EOF":
                return output
            output += current.letter
            current = parent
    return output



# Depress the text
def depress(string, bi_dict):
    
    # Use the functions to depress the file
    parent = makeMap(bi_dict)
    binary = makeBinary(string)
    output = makeText(binary, parent)
    return output

