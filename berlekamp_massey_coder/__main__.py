import random

from .rs_decoding import rs_decode_msg
from .rs_encoding import rs_encode_msg

D = 9
N = 31
k = N - D + 1

message = b"Hi my friends! How are you?"
msglen = len(message)

print("Message: \n")
print(message)

print("Original:  ")
original = bytearray(message)
print(*original, sep=" ")

encoded = rs_encode_msg(original, N - k)

print("\nEncoded:   ")
print(*encoded, sep=" ")

encoded_str = [x for x in encoded]
erroneous = list(encoded_str)

print("\nErroneous: ")

random.seed()
for i in range(min((N - k) // 2, len(encoded))):
    h = random.randint(0, msglen - 1)
    r = random.randint(0, 255)
    erroneous[h] = r

print(*erroneous, sep=" ")

decoded = rs_decode_msg(erroneous, N - k)  # N-k
print("\n")

print("decoded: ")
print(*decoded, sep=" ")

print()
for i in range(min(msglen, len(decoded))):
    char_value = decoded[i]
    char_symbol = chr(char_value)
    print(char_symbol, end="")
