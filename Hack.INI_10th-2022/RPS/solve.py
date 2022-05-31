from pwn import *

r = remote("rps.challs.shellmates.club", 443, ssl=True)

def res(a, b):
    if a == b:
        return "D"
    if a == "P" and b == "R":
        return "A:3"
    if a == "S" and b == "P":
        return "A:3"
    if a == "R" and b == "S":
        return "A:3"
    if b == "P" and a == "R":
        return "B:3"
    if b == "S" and a == "P":
        return "B:3"
    if b == "R" and a == "S":
        return "B:3"

def calc_round(alice, bob):
    alice_input = alice.split(b" ")[1].decode().strip()
    bob_input = bob.split(b" ")[1].decode().strip()
    alice_score = 0
    bob_score = 0
    alice_last_score = 0
    bob_last_score = 0
    for i in range(len(alice_input)):
        result = res(alice_input[i], bob_input[i])
        if result == "D":
            alice_score += 1
            bob_score += 1
            alice_last_score = 0
            bob_last_score = 0
        elif result.split(":")[0] == "A":
            bob_last_score = 0
            if alice_last_score == 0:
                alice_last_score = 3
                alice_score += 3
            else:
                alice_last_score *= 2
                alice_score += alice_last_score
        elif result.split(":")[0] == "B":
            alice_last_score = 0
            if bob_last_score == 0:
                bob_last_score = 3
                bob_score += 3
            else:
                bob_last_score *= 2
                bob_score += bob_last_score
    if alice_score > bob_score:
        return f"A:{alice_score}".encode()
    elif alice_score < bob_score:
        return f"B:{bob_score}".encode()
    else:
        return "D".encode()

while True:
    alice = r.recvline()
    print(alice)
    bob = r.recvline()
    print(bob)
    result123 = calc_round(alice, bob)
    print(result123)
    r.sendline(result123)
    print(r.recvline())