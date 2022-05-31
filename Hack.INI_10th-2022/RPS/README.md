# from RPS

## Description:

> Tags: scripting

>Alice and Bob were playing rock paper scissors.
They forget to calculate the score at each round.
Can you help them you determine the winner at the end of each game. The rules are simple: In each round if a player wins, he gets 3 points.
If he wins in the next round he gets the double of the point he got in the last round.
In case of draw, both players will get 1 point.
the output format will be the first letter of the player's name (A or B) followed
by the score he got example : 'A:1337' Alice won and got 1337 points.
in case of a drawn game just print 'D'

> Author : yh_0x7

> ncat -v --ssl rps.challs.shellmates.club 443

## First thoughts:

The script that will solve the challenge should be easy to write. We have to take in mind all the possible cases.

## The algorithm:

The [script I used](solve.py).

and I got the flag:
```
shellmates{17'5_J57_r0cK_P4P3r_5c1550R5}
```