"""
Connie Xu
Hill Cipher
AP CSP
Assumptions: The user puts in the correct input of only letters and " " in their message. **NO PUNCTUATION**
"""

import random


ALPHABET = "abcdefghijklmnopqrstuvwxyz !;" #29 charcters for ease of inversing
KEYLENGTH = 9 #The key matrix is a pre-established 3x3 which makes 9 numbers in all
SPACE = 28 #space is at index 28 in ALPHABET
ROWS = 3 #The amount of rows
FIRST = 0 #This will be used to obtain the first index or number


def generateInputMatrix(user): #The user inputs a string and it returns the matrix of the string and turning the string into integers (0-28)
    
    #input matrix: whatever the user inputs
    
    if len(user) < KEYLENGTH: #This is because the input matrix will not be long enough (giving you the out of bounds error) unless it is the length of the key and the key has an established amount of numbers of 9 (3x3)
        for i in range(KEYLENGTH - len(user)): #If the message is shorter than the key, it will append spaces to the end of the message until it reaches 9 in length
            user += " "
            
    letterList = [] 
    for i in range(len(user)): 
        temp = user[i] 
        number = ALPHABET.index(temp) #Changes each individual letter into integers from 0-29 (after the alphabet + the space, the other symbols are used because inversing a prime number simplifies the problem.  
        letterList.append(number)

    """
    The intent of the filler is easily explained with an example:
    Take the message 'hello'. Because we have pre-established that the matrix will have 3 rows, without another character, the matrix multiplication and basically everything related to this program would cease to work.

    h l
    e o
    l _
    
    As depicted by the underscore, we have nothing there. This is problematic and thus, the 'filler' would fix this problem by appending the space which happens to be the index of 28 in the constant, ALPHABET
    Of course, this short of a message would have been fixed by the above by filling it until 9 letters, however, this is just to show an example of how it works.
    """
    filler = (ROWS - (len(user) % ROWS)) % ROWS #gets the filler if the message that the user inputs is not divisible by 3. 
    for i in range(filler): #This only adds a filler if it needs a filler
        letterList.append(SPACE) #puts in a space
        
    finalList = [[], [], []] #3 row matrix
    for i in range(len(user)): 
        math = i % ROWS #This math generates the different lists in the 2D list that it will be placed in (whether it is list 1, list 2, list 3)
        finalList[math].append(letterList[i]) #This appends the message (in integers) into the final matrix form for the message.

    return finalList

    
def generateKeyMatrix(): #This creates the key which is what the message matrix will be multiplied by. This is randomly generated.
    determinant = 0 
    while (determinant == 0): #If the determinant is zero, then there is no inverse of that matrix. Therefore, a new matrix must be generated.
        keyMatrix = [[], [], []] #This sets up an empty matrix for the 'key' matrix
        
        for i in range(KEYLENGTH): #This is to generate the 'key' matrix
            randomNum = random.randint(0, len(ALPHABET) - 1) #This helps establish which numbers are used from 0-28 because of the ALPHABET constant, as we can choose any number from there
            keyMatrix[i % ROWS].append(randomNum) #appends to the actual key matrix to establish the key matrix

        #check if matrix has an inverse
        determinant = checkDeterminant(keyMatrix) #If the determinant is not 0, then it will break the loop and return the key matrix.

    return keyMatrix

    
def checkDeterminant(matrix): #This does all the determinant math.
    """
    This is derived from the formula on this page: https://www.mathworks.com/help/aeroblks/determinantof3x3matrix.html
    """
    determinant = matrix[0][0]*matrix[1][1]*matrix[2][2] - matrix[0][0]*matrix[1][2]*matrix[2][1] - matrix[0][1]*matrix[1][0]*matrix[2][2] - matrix[0][1]*matrix[1][2]*matrix[2][0] + matrix[0][2]*matrix[1][0]*matrix[2][1] - matrix[0][2]*matrix[1][1]*matrix[2][0]
    
    return determinant

    
def matrixMultiplication(key, matrix): #This is where the math happens to ENCRYPT the message matrix
    encryptedMessage = [[0 for i in range(len(matrix[0]))] for i in range(ROWS)] #This intializes a matrix filled with a 0 at each position that is the same size as the message matrix
    for i in range(len(encryptedMessage)): #This takes the length of the columns
        for j in range(ROWS): #This takes the rows going down
            for k in range(ROWS): 
                encryptedMessage[j][i] = (encryptedMessage[j][i] + key[j][k] * matrix[k][i]) % len(ALPHABET) #This is derived from matrix multiplication — essentially all the math related to it
    """
    Since I want to move vertically down, it needs to be set up like [j][i] because this gives the column and then the row as i goes through horizontally
    and j goes through vertically.
    The third for loop is there so that it can iterate through the positions to go through the multiplication. Then, modulus division is used so that
    it can be in the range of the predetermined numbers from ALPHABET (as this is how it will convert BACK to characters).
    """
    
    return encryptedMessage


def convertToLetters(m): #This converts our now encrypted number message into an encrypted string message.
    stringMessage = ""
    
    for i in range(len(m[FIRST])* len(m)): #length of columns * length of rows
        math = i % ROWS #helps put it in the right position
        stringMessage += ALPHABET[m[math][FIRST]] #String concatenation occurs here. It takes the integer at the matrix in the encrypted number matrix and finds the corresponding letter.
        m[math].pop(FIRST) #By popping off the first (slash deleting the first number in the index) it eliminates the problem of iterating through the matrix which would have been a pain to code.

    return stringMessage


def main():
    userInput = input("Please type your message (ONLY LETTERS AND SPACES): ").lower() #Simplifies life; only working with lowercase letters
    inputMatrix = generateInputMatrix(userInput) 
    keyMatrix = generateKeyMatrix()
    message = matrixMultiplication(keyMatrix, inputMatrix)
    stringMessage = convertToLetters(message)
    print("Your encrypted message is: " + stringMessage)

    
main()
    
