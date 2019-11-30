import string
import random

def generatePNR(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


print(generatePNR())
