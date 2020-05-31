### Challenge Info

​	The challenge is a crypto challenge from the pwn2win event , it's focused on the symmetric cryptography and especially the aes block cipher.So we are given remote connection   `nc encryption.pwn2.win 1337`  and the python script that is running in the remote `server.py`  .

### Writeup Summary

- #### gain general information 

- #### deep look into encrypt your secret 

- #### solution 

### general information 

​	By the first look at the `server.py` script we notice there are 3 main functions first one is `def encrypt(txt, key, iv)` where you pass the plaintext the key and iv this function will check that the plaintext length is multiple of Block Size which is 128 and then it will encrypt the plaintext with custom implementation of AES , the second one is `enc_plaintext`this function that we will interact with it will take our plaintext and decode it as a base64 and pass it to `encrypt` with `key1` and `iv1` which are secrets . The last function is `enc_flag()` it will encrypt the flag with `key2` and `iv2` which their difinition is :

```python
iv2 = AES.new(key1, AES.MODE_ECB).decrypt(iv1)
key2 = xor(to_blocks(flag))
```

by looking at the `xor` function we noticed that if two parametres  `a,b` are passed then it will calculate `a xor b` else if one parametre `a` is passed it will return `a[0] xor \x00 *len(a[0])` so it will return the first block xored with 00 and that meen it will return the first block .

###  deep look into encrypt your secret 

​	After looking in the function i noticed it doing 2 things interesting : 

- first thing is that it is returning to us the iv passed in parametre + the cipher so for example if we passed `iv2` to the function than we get as a result `iv2+ cipher` 

  ```python
  base64.b64encode(iv+ctxt)
  ```

  PS: of course all inputs and outputs are encoded with base64

- the second  interesting thing is that it is overriding the `iv2` and `key2` that are used in encrypting the flag :

  ```python
  iv2 = AES.new(key2, AES.MODE_ECB).decrypt(iv2)
  key2 = xor(to_blocks(ctxt))
  ```

  so the new `iv2` is the decryption of the previous `iv2` with `key2` and the new `key2` is the xor of the cipher calculated and as we have discussed `xor` function when we pass one parametre it will return the first block of the passed object  so `key2 = cipher[0]` so from the result `iv+ctx ` we can get `iv1 ` and `key2` from the cipher and to get the next value of `iv2` we need the value of `key2` before change .so the idea of the challenge is to try to guess the `iv2` and `key2` that will be used next time we encrypt the flag .

### Solution

​	after trying in a paper the different combination of commandes that will allow us to get the key and initial vector i finnaly found the solution it is bit tricky so what we will do is :

1. we will send a random payload with 16 bytes  to the oracle that will return us `iv1 + cipher` and from the cipher we can get  the new value `key2` because as we said `key2 = a[0]` the new key is the first block of cipher 

2. next we will send the encrypt flag command that will return to us  `iv2 + flag_cipher` and here we can use the result of the first step which is key2 and get the new value of `iv2` because it will be changed by `iv2 = AES.new(key2, AES.MODE_ECB).decrypt(iv2)`  and also we update the value of `key2` now we have the `key2` and `iv2` values and we can use it to decipher the flag next time because this value will be used next time 

3. we will send the encrypt flag command and decrypt the cipher :

   ```python
   aes = AES.new(key2, AES.MODE_ECB)
   curr = iv2
   bs = len(key2)
   text=b""
   for block in blocks:
       text +=xor(curr, aes.decrypt(block))
       curr = xor(text[-bs:], block)
   print(text)
   ```

   the challenge used a modified version of aes ecb it work like this `cipher1 = aes(text1 xor iv)` then `cipher2 = aes(text2 xor (text1 xor cipher1))` and it do this for each block . so for the decryption part we can do this 

   `text1 = iv xor aes.decrypt(cipher1)` and for other blocks `textI= (cipherJ xor textJ) xor aes.decrypt(cipherI) ` where `J = I-1`.

and finnaly we got the flag `CTF-BR{kn3W_7h4T_7hEr3_4r3_Pc8C_r3pe471ti0ns?!?}` . awesome challenge had so much fun solving it *.*

​    