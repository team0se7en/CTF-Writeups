from pwn import *
import re
r = remote("chall.csivit.com", 30431)
received = r.recvuntil("Enter username hex string :").decode()
found = re.findall(r'[a-z0-9]{64}', received)
username = found[0]
password = found[1]
log.info("Received Response from server")
log.info("Username hex cipher = {}".format(username))
log.info("Password hex cipher = {}".format(password))
flipping = log.progress("Flipping Byte number 6 ")
username_bytes = bytearray.fromhex(username)
password_bytes = bytearray.fromhex(password)
username_bytes[6] = username_bytes[6] ^ ord("?") ^ ord("s")
password_bytes[6] = password_bytes[6] ^ ord("?") ^ ord("t")
flipping.success("Flipping finished")
username = username_bytes.hex()
password = password_bytes.hex()
log.info("Sending username payload = {}".format(username))
r.sendline(username)
r.recvuntil("Enter password hex string :")
log.info("Sending password payload = {}".format(password))
r.sendline(password)
log.success(r.recvline().decode())
