# magic

## Description:

> Tags: easy/medium

>Only true wizards can find my magic secret.
The flag looks like: shellmates{magic_secret}.

> Author : Muhammad

> Files : [chall](chall)

## First thoughts:

The binary asks for a secret and it check if it's correct.

## Reversing the binary:

For the reversing part, I used `Ghidra Decompiler`.

We open the binary with `Ghidra` and let it detect and decompile the binary for us. Taking a look at it's functions, we find the `main` function.

```c

undefined8 main(void)

{
  int iVar1;
  long in_FS_OFFSET;
  undefined local_28 [24];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("You think that you found my magic secret?\nTry it out : ");
  __isoc99_scanf(&DAT_00102040,local_28);
  iVar1 = compare_with_secret(local_28);
  if (iVar1 == 0) {
    puts("Wrong! Try again!");
  }
  else {
    puts("Congrats you wizard!");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}

```

Analyzing the code, we found out that the program asks for a secret and sends it to the function `compare_with_secret`.

Checking the code and renaming some variables we got:

```c

bool compare_with_secret(void *input)

{
  int _0_to_3;
  long in_FS_OFFSET;
  byte local_142;
  char i;
  FILE *exe_file;
  undefined8 local_138;
  undefined8 local_130;
  undefined2 local_128;
  undefined local_126;
  char local_118 [264];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_138 = 0x670b7112190a093a;
  local_130 = 0x193f202b3f0e1a1c;
  local_128 = 0x145;
  local_126 = 0;
  memset(local_118,0,0x100);
  readlink("/proc/self/exe",local_118,0xff);
  exe_file = fopen(local_118,"rb");
  for (i = 0; i < 18; i = i + 1) {
    _0_to_3 = mudolo((int)i,4);
    fseek(exe_file,(long)_0_to_3,0);
    fread(&local_142,1,1,exe_file);
    *(byte *)((long)input + (long)i) = local_142 ^ *(byte *)((long)input + (long)i);
  }
  _0_to_3 = memcmp(&local_138,input,0x12);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return _0_to_3 == 0;
}
```

So what is happening here is: 
 
 - Reading `/proc/self/exe` file.
 - looping from 0 to 17 and on it:
    
    - Getting the modulo of `i` and `4` and putting it in `_0_to_3`.
    - Getting the `_0_to_3`th byte of the file `exe`.
    - Xoring it with the `i`th character from our input.
 - And finally comparing the modified input and the data we have in `&local_138`.

## Solving the challenge:

We need to get the first 4 of the file `exe`, and the way I done it was using `GDB`, so I added a breakpoint in the function, send `aaaaaaaa` as the input, and check it's xoring result:

```
*RCX  0x7fffffffd980 ◂— 0x272d241e272d241e
```

and so, I xored `aaaaaaaa` with `0x272d241e272d241e` and got
```py
[0x7f, 0x45, 0x4c, 0x46]
```

and finally to get the secret we xor the bytes with `&local_138`, and we get:

```
ELF_m4G!c_ByTes_:D
```

and the flag is:

```
shellmates{ELF_m4G!c_ByTes_:D}
```
