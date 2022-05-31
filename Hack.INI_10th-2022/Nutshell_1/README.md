# Nutshell1

## Description:

> Tags: medium zsh

> I created my own script, make sure to read it well.

> Author : badsUwU

> ncat -v --ssl nutshell1.challs.shellmates.club 443

> Files : [nutshell1](nutshell1)

## First thoughts:

The challenge is a Linux challenge and we were provided with a `zsh script`.

The scripts asks for two inputs, tests them and when it's given the right inputs it should return the flag.

## Reading the script:

The script asks for an input `v1`, and provides it to the `read command`, which when it's executed, it stores its input in `v2`.

After that, the scripts tests if both of the inputs are not empty.

Our goal is to read the flag, so one of the inputs must be `cat flag`.

As we noticed, the `v1` variable must be accepted when it's added to the `read` command. So searching for `zsh read command` we found that it accepts the parameter `-e`, which echos the provided input to the standard output, and so the input will be assigned to `v2`, and finally it will be executed.

## Solving the challenge:

Passing `-e` and `cat flag` to the first and second input respectively, we get the flag:

```
shellmates{nUt$H3ll_1_PWnED}
```