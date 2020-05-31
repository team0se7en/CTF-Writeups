import base64
from Crypto.Cipher import AES
from pwn import  *

BLOCK_SIZE = 16
def to_blocks(txt):
    return [txt[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE] for i in range(len(txt)//BLOCK_SIZE)]


def xor(b1, b2=None):
    if isinstance(b1, list) and b2 is None:
        assert len(set([len(b) for b in b1])) == 1, 'xor() - Invalid input size'
        assert all([isinstance(b, bytes) for b in b1]), 'xor() - Invalid input type'
        x = [len(b) for b in b1][0]*b'\x00'
        for b in b1:
            x = xor(x, b)
        return x
    assert isinstance(b1, bytes) and isinstance(b2, bytes), 'xor() - Invalid input type'
    return bytes([a ^ b for a, b in zip(b1, b2)])
r = remote("encryption.pwn2.win", 1337)
r.recvuntil("Choice: ")
r.sendline("1")
r.recvuntil("Plaintext: ")
payload = b"A"*BLOCK_SIZE
print("[*] Sending First Random Payload")
r.sendline(base64.b64encode(payload))
print("[*] Received the encryption ")
received = r.recvuntil("Choice: ").decode().split('\n')[0]
received_bin= base64.b64decode(received)
key2 = xor(to_blocks(received_bin[16:]))
print("[*] constructing the key2")
r.sendline("2")
print("[*] Sending the get flag command")
flag_received = base64.b64decode(r.recvuntil("Choice: ").decode().split('\n')[0])
iv2 = flag_received[:16]
iv2 = AES.new(key2, AES.MODE_ECB).decrypt(iv2)
key2 = xor(to_blocks(flag_received[16:]))
print("[*] Received the flag encrypted ")
print("[*] Constructing the new iv2 and key2")
r.sendline("2")
print("[*] Sending the get flag command")
flag_received = base64.b64decode(r.recvuntil("Choice: ").decode().split('\n')[0])
blocks = to_blocks(flag_received[16:])
print("[*] flag encrypted received ")
aes = AES.new(key2, AES.MODE_ECB)
curr = iv2
bs = len(key2)
print("[*] Decrypting the flag with the key2 and iv2")
text=b""
for block in blocks:
    text +=xor(curr, aes.decrypt(block))
    curr = xor(text[-bs:], block)
print("[*] Flag decrypted congratulation {}".format(text))
