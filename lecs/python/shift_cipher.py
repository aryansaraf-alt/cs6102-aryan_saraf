##shift cipher, implementation and breaking
## ciphertext-only ATTACK.
import random

K = list(range(26))

M = list(range(26))


def KGen():
    return random.randint(0, 25)


k = KGen()

print("random key for ts round: ", k)

pt = input("input plaintext to be encrypted: ")  # can be hardcoded to break cipher.


def enc(pt, k):
    ct = ""
    pt = pt.upper()
    for char in pt:
        num = ord(char) - 65
        shift = (num + k) % 26
        ct += chr(shift + 65)
    return ct


def dec(ct, k):
    pt = ""
    for char in ct:
        num = ord(char) - 65
        shift = (num - k) % 26
        pt += chr(shift + 65)
    return pt


ciphertext = enc(pt, k)

print(ciphertext)

decrypted = dec(ciphertext, k)

print(decrypted)
