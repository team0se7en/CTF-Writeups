# Nutshell2

## Description:

> Tags: medium

> Counting backwards ?

> Author : badsUwU

> ncat -v docker.shellmates.club $INSTANCE_PORT

> Files : [nutshell2](nutshell2)

## First thoughts:

The challenge is a Linux challenge and we were provided with a `bash script`.

The scripts asks for one input, and if it's correct, it executes `cat flag`.

## Reading the script:

The script asks for an input `v1`, and provides it to the `touch command`, which when it's executed, it creates a file with the input provided.

After that, the scripts tests if a file with the name `nutshell_file` exists. If it is, it reads its `BIRTH` and `MODIFY` datetime using `stat` and checks if `BIRTH` is greater then `MODIFY`.

Our goal is to create the file `nutshell_file`, and make its `BIRTH` is greater then `MODIFY` datetime.

## Solving the challenge:

I searched for `touch` parameters, and I didn't find a way to change the `BIRTH` datetime, but I found how to set the `MODIFY` datetime. The default value for `BIRTH` is 0, so if we set `MODIFY` to -1 it should work.

> Note: running `touch` in my machine, I wasn't able to change the `BIRTH` datetime, and it was always getting the value 0, but in the server, the `BIRTH` datetime was set to the date the file was created, and I think I read something about `ext4` and it's relation with `BIRTH`, but I'm not sure.

Passing `-d @-1 nutshell_file` to the first input, we get the flag:

```
shellmates{nUt$H3ll_2_PWnED_vkfdnvjfk}
```
