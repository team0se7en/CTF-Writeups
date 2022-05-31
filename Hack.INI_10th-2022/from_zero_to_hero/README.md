# from zero to hero

## Description:

> Tags: medium

>Start your journey and be the one who learns them all.

> Author : Ouxs

> ncat -v --ssl zero-to-hero.challs.shellmates.club 443

## First thoughts:

After we connect to the given server, a list of skills is given in the following pattern:

```
To learn {skill} you must know : {skill1-skill2 ...}
```
... and we are asked to order the skills in such an order that:

 - all the skills must be acquired.
 - the skills should be separated with `-`.

However, if it's impossible to find an order, we reply with `impossible`

## The algorithm:

For this challenge, I used `graphlib`, which is a Python library that implements graph theory algorithms. And one of it's classes is `TopologicalSorter`, which is what we need for this problem.

The [script I used](solve.py).

and I got the flag:
```
shellmates{T0POLOGICAL_$0RTING_FTW____!!!}
```