# chess.INI

## Description:

> Tags: programming scripting medium/hard

>Did you heard about chess!!! sure you did. Your mission now is to find the length of path that the king (K) takes to reach the target (T). the pawns (p) are like obstacles that the king can't pass. learn more about king's moves here : https://en.wikipedia.org/wiki/King_(chess)

> Author : yh_0x7

> ncat -v --ssl chess-ini.challs.shellmates.club 443

## First thoughts:

In this challenge, a chess board is given and the goal is to count how many steps it's required for the king `K` to get to the target `T`.

So it's a path finding challenge in all the eight directions.

## The algorithm:

I used a BFS path finding on matrix algorithm that I got from the good old geeksforgeeks, but it only included 4 directions (up, down, left, right), so I added the other 4 directions.

The [script I used](solve.py).

and I got the flag:
```
shellmates{ch355_M4k35_M3n_w153r_4nd_CL34R-519H73D}
```