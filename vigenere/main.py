#Constants
ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
TABLE = [
    ["N", "Z", "R", "Y", "J", "V", "K", "M", "U", "D", "W", "A", "X", "P", "L", "Q", "H", "G", "S", "F", "C", "I", "O", "T", "E", "B"],
    ["Y", "J", "V", "K", "M", "U", "D", "W", "A", "X", "P", "L", "Q", "H", "G", "S", "F", "C", "I", "O", "T", "E", "B", "N", "Z", "R"],
    ["R", "Y", "J", "V", "K", "M", "U", "D", "W", "A", "X", "P", "L", "Q", "H", "G", "S", "F", "C", "I", "O", "T", "E", "B", "N", "Z"],
    ["J", "V", "K", "M", "U", "D", "W", "A", "X", "P", "L", "Q", "H", "G", "S", "F", "C", "I", "O", "T", "E", "B", "N", "Z", "-", "Y"],
    ["F", "C", "I", "O", "T", "E", "B", "N", "Z", "R", "Y", "J", "V", "K", "M", "U", "D", "W", "A", "X", "P", "L", "Q", "H", "G", "S"],
    ["D", "W", "A", "X", "P", "L", "Q", "H", "G", "S", "F", "C", "I", "O", "T", "E", "B", "N", "Z", "R", "Y", "J", "V", "K", "M", "U"],
    ["A", "X", "P", "L", "Q", "H", "G", "S", "F", "C", "I", "O", "T", "E", "B", "N", "Z", "R", "Y", "J", "V", "K", "M", "U", "D", "W"],
    ["B", "N", "Z", "R", "Y", "J", "V", "K", "M", "U", "D", "W", "A", "X", "P", "L", "Q", "H", "G", "S", "F", "C", "I", "O", "T", "E"],
    ["P", "L", "Q", "H", "G", "S", "F", "C", "I", "O", "T", "E", "B", "N", "Z", "R", "Y", "J", "V", "K", "M", "U", "D", "W", "A", "X"],
    ["K", "M", "U", "D", "W", "A", "X", "P", "L", "Q", "H", "G", "S", "F", "C", "I", "O", "T", "E", "B", "N", "Z", "R", "Y", "J", "V"],
    ["T", "E", "B", "N", "Z", "R", "Y", "J", "V", "K", "M", "U", "D", "W", "A", "X", "P", "L", "Q", "H", "G", "S", "F", "C", "I", "O"]
]


#-------------------------------------------------------------------------------
def getFileText(file):
    return open(file, "r").read().replace(" ", "").replace("\n", "")


#-------------------------------------------------------------------------------
def calcKeySize(text, numPatterns):
    locations = []
    distances = []

    # Locate all patterns
    for i in range(len(text)):
        pattern = text[i: i + numPatterns]

        if len(pattern) < numPatterns:
            break

        locations.append([])
        find = text.find(pattern, 0)
        while find != -1:
            locations[i].append(find)
            find = text.find(pattern, find + 1)

        if len(locations[i]) > 1:
            for j in range(1, len(locations[i])):
                distances.append(locations[i][j] - locations[i][0])

    # Get the greatest common divisor
    if len(distances) < 2:
        return distances[0]

    gcdArr = gcd(distances[0], distances[1])

    for i in range(2, len(distances)):
        gcdArr = gcd(distances[i], gcdArr)

    return gcdArr


#-------------------------------------------------------------------------------
# http://en.wikipedia.org/wiki/Euclidean_algorithm
def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


#-------------------------------------------------------------------------------
def divideText(text, keySize):
    count = 0
    textChunks = ""
    dividedText = []

    for i in text:
        if count == keySize:
            dividedText.append(textChunks)
            textChunks = i
            count = 1
        else:
            textChunks += i
            count += 1

    return dividedText


#-------------------------------------------------------------------------------
def dominantLettersByColumn(dividedText, keySize):
    # Create empty array
    dominances = []
    for i in range(keySize):
        dominances.append([["A", 0], ["B", 0], ["C", 0], ["D", 0], ["E", 0], ["F", 0], ["G", 0], ["H", 0], ["I", 0], ["J", 0], ["K", 0], ["L", 0], ["M", 0], ["N", 0], ["O", 0], ["P", 0], ["Q", 0], ["R", 0], ["S", 0], ["T", 0], ["U", 0], ["V", 0], ["W", 0], ["X", 0], ["Y", 0], ["Z", 0]])

    for i in range(len(dividedText)):
        for j in range(keySize):  # keySize times
            for k in range(len(dominances[j])):  # 26 times
                if (dividedText[i][j].upper() == dominances[j][k][0]):
                    dominances[j][k][1] += 1
                    break

    # Dominance by column table (from most dominant to lower dominant)
    print "\nDominance by column table"
    for i in range(len(dominances)):
        dominances[i].sort(key=lambda x: x[1], reverse=True)

    for i in range(len(dominances)):
        print "\nColumn", i
        for j in range(len(dominances[i])):
            print dominances[i][j][0], "--->", dominances[i][j][1]


#-------------------------------------------------------------------------------
def decipherText(dividedText):
    decipheredText = ""
    for i in dividedText:
        pos = 0
        for j in range(len(i)):
            cipheredLetter = i[j].upper()
            if(cipheredLetter in TABLE[pos]):
                letterIndex = TABLE[pos].index(cipheredLetter)
                decipheredText += ALPHABET[letterIndex].lower()

            pos += 1

    print "\nDeciphered text:"
    print "------------------"
    print decipheredText


#-------------------------------------------------------------------------------
def main():
    print "-------------------------"
    print "Homework#1 - Cryptography"
    print "-------------------------"

    file = "cipher.txt"
    numPatterns = 5
    keySize = 0

    text = getFileText(file)
    keySize = calcKeySize(text, numPatterns)
    dividedText = divideText(text, keySize)

    print "\nKey size:", keySize

    dominantLettersByColumn(dividedText, keySize)
    decipherText(dividedText)


#-------------------------------------------------------------------------------
# to run the function if needed
if __name__ == "__main__":
    main()
