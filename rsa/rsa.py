import random
import sys


#-------------------------------------------------------------------------------
# Calculate logarithms
def log(x, base):
    count = -1

    while x > 0:
        x /= base
        count += 1
        if x == 0:
            return count


#-------------------------------------------------------------------------------
# Computes the modular multiplicative inverse
def extendedEuclid(d, f):
    x1, x2, x3 = 1, 0, f
    y1, y2, y3 = 0, 1, d

    while True:
        if y3 == 0:
            raise ValueError
        if y3 == 1:
            return y2

        q = x3 / y3
        x1, x2, x3, y1, y2, y3 = y1, y2, y3, (x1 - q * y1), (x2 - q * y2), (x3 - q * y3)


#-------------------------------------------------------------------------------
# Rabin Miller primality test
def rabinMiller(n):
    s = n - 1
    t = 0

    while s & 1 == 0:
        s = s / 2
        t += 1

    k = 0

    while k < 128:
        a = random.randrange(2, n - 1)
        v = pow(a, s, n)
        if v != 1:
            i = 0
            while v != (n - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % n
        k += 2

    return True


#-------------------------------------------------------------------------------
# Check if a number is prime
def isPrime(n):
    #lowPrimes is all primes (without 2, which is covered by the bitwise and operator) under 1000.
    #taking n modulo each lowPrime allows us to remove a huge block
    #of composite numbers from our potential pool without resorting to Rabin-Miller
    lowPrimes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
                 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167,
                 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
                 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353,
                 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449,
                 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563,
                 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653,
                 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761,
                 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877,
                 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    if n >= 3:
        if n & 1 != 0:
            for p in lowPrimes:
                if n == p:
                    return True
                if n % p == 0:
                    return False
            return rabinMiller(n)

    return False


#-------------------------------------------------------------------------------
# Generate large prime numbers
def generateLargePrimes(size):
    r = 100 * (log(size, 2) + 1)

    while r > 0:
        n = random.randrange(2 ** (size - 1), 2 ** (size))
        r -= 1
        if isPrime(n) is True:
            return n

    raise OverflowError


#-------------------------------------------------------------------------------
# Extracts the components of the keys (n, d) or (n, e)
def extractComponents(keyFilename):
    file = open(keyFilename, "r")
    content = file.readline()
    components = str.split(content, ",")

    return int(components[0]), int(components[1])


#-------------------------------------------------------------------------------
# http://en.wikipedia.org/wiki/Euclidean_algorithm
def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t

    return a


#-------------------------------------------------------------------------------
# Returns a tuple (r, t) | n = r*2^t
def removeEven(n):
    if n == 0:
        return (0, 0)

    r = n
    t = 0

    while (r & 1) == 0:
        t = t + 1
        r = r >> 1

    return (r, t)


#-------------------------------------------------------------------------------
# Returns a non-trivial sqrt(1) mod n, or None
def getRootOne(x, k, n):
    r, t = removeEven(k)
    oldi = None
    i = pow(x, r, n)

    while i != 1:
        oldi = i
        i = (i * i) % n

    if oldi == n - 1:
        return None

    return oldi


#-------------------------------------------------------------------------------
# Returns a tuple (p, q) that are the prime factors of n
def factorRsa(e, d, n):
    k = e * d - 1
    y = None

    while not y:
        x = random.randrange(2, n)
        y = getRootOne(x, k, n)

    p = gcd(y - 1, n)
    q = n // p

    return (p, q)


#-------------------------------------------------------------------------------
def generate(size, name):
    print "Generating keys..."

    while True:
        try:
            p = generateLargePrimes(size)
            q = generateLargePrimes(size)
            n = p * q
            break
        except OverflowError:
            pass

    t = (p - 1) * (q - 1)

    while True:
        try:
            e = random.randrange(t)
            x = extendedEuclid(e, t)
            break
        except ValueError:
            pass

    d = x % t

    filename = name + ".pub"
    file = open(filename, "w+")
    file.write(str(n) + "," + str(e))

    filename = name + ".priv"
    file = open(filename, "w+")
    file.write(str(n) + "," + str(d))

    print "Generate complete!"


#-------------------------------------------------------------------------------
def cypher(message, outputFilename, name):
    print "Cyphering message..."

    n, e = extractComponents(name + ".pub")
    nbl = n.bit_length() - 1
    block = ""
    zerosOnly = True
    numOfZeros = 0

    for i in range(len(message)):
        if message[i] == "0" and zerosOnly:
            numOfZeros = numOfZeros + 1
        if message[i] == "1":
            zerosOnly = False

        block = block + message[i]

        if len(block) == nbl:
            c = pow(int(block, 2), e, n)
            binCount = bin(numOfZeros)[2:]
            bc = bin(c)[2:].zfill(n.bit_length())

            glue = str(bc) + str(binCount)
            block = ""
            zerosOnly = True
            numOfZeros = 0

    if block != "":
        c = pow(int(block, 2), e, n)
        bincount = bin(numOfZeros)[2:]
        bc = bin(c)[2:]

        bc = bc.zfill(n.bit_length())

        glue = str(bc) + str(bincount)

    file = open(outputFilename, "w+")
    file.write(glue)


#-------------------------------------------------------------------------------
def decypher(cypherMessage, outputFilename, name):
    print "Decyphering message..."

    n, d = extractComponents(name + ".priv")
    message = str.split(cypherMessage, "\n")
    count = 0

    for i in message:
        if i == "":
            break

        cut = n.bit_length()
        block = i[:cut]

        count = i[cut:]
        if count != "":
            icount = int(count, 2)
            c = pow(int(block, 2), d, n)
            bc = bin(c)[2:]
            bc = bc.zfill(icount + len(bc))
            file = open(outputFilename, "w+")
            file.write(bc)


#-------------------------------------------------------------------------------
def reveal(name):
    print "Revealing components..."

    n, e = extractComponents(name + ".pub")
    n, d = extractComponents(name + ".priv")
    p, q = factorRsa(e, d, n)

    print "prime p: " + str(p)
    print "\nprime q: " + str(q)
    print "\nint e: " + str(e)
    print "\nint d: " + str(d)


#-------------------------------------------------------------------------------
def help():
    print "The commands available are:"
    print "\nGenerate: python rsa.py -generate -size x -name n"
    print "\nCypher: python rsa.py -cypher -key n -i fi -o fo"
    print "\nDecypher: python rsa.py -decypher -key n -i fi -o fo"
    print "\nReveal: python rsa.py -reveal -key n"


#-------------------------------------------------------------------------------
def chooseOption(option):
    if option == "-generate":
        try:
            size = int(sys.argv[3])
            name = sys.argv[5]
            generate(size, name)
        except:
            help()

    elif option == "-cypher":
        try:
            message = open(sys.argv[5], "r").read()
            outputFilename = sys.argv[7]
            name = sys.argv[3]
            cypher(message, outputFilename, name)
        except:
            help()

    elif option == "-decypher":
        try:
            cypherMessage = open(sys.argv[5], "r").read()
            outputFilename = sys.argv[7]
            name = sys.argv[3]
            decypher(cypherMessage, outputFilename, name)
        except:
            help()

    elif option == "-reveal":
        name = sys.argv[3]
        reveal(name)

    else:
        help()


#-------------------------------------------------------------------------------
def main():
    print "------------------"
    print "RSA - Cryptography"
    print "------------------"

    try:
        option = sys.argv[1]
        chooseOption(option)
    except:
        help()


#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
