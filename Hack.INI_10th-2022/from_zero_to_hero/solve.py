from pwn import *
from graphlib import *
r = remote("zero-to-hero.challs.shellmates.club", 443, ssl=True)

def get_task(line):
    task_name = line.split()[2]
    tasks = []
    if line.split()[-1] != ":":
        tasks = set(line.split()[-1].split("-"))
    return [task_name, tasks]

r.recvuntil(b"Note : skills' names are generated randomly\n")
r.recvline()
c = 0
while True:
    print(c)
    if c == 90:
        print(r.recvall())
        r.interactive()
    lines = r.recvuntil(b"Path ->").split(b"\n")
    graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
    tasks = []
    constraints = {}
    for i in range(len(lines)-1):
        res = get_task(lines[i].decode("utf-8"))
        tasks.append(res[0])
        if res[1] != []:
            constraints[res[0]] = res[1]
        else:
            constraints[res[0]] = {}
    ts = TopologicalSorter(constraints)
    try:
        result = tuple(ts.static_order())
        r.sendline("-".join(result).encode())
    except:
        print("impossible")
        r.sendline(b"impossible")
    c+=1