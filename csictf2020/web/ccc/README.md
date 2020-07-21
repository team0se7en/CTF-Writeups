## Challenge Info 

Web challenge `http://chall.csivit.com:30215/` 

## Writeup summary

- gain general informations 
- deep look into login
- deep look into /adminNames  
- sign custom jwt and get flag

### gain general informations

first when we open the website we got a home page with a navigation bar redirecting to different pages  the only working pages are  `Our Admin` ->`/adminNames`  , `Login` -> `/login`  all the others take to the home page 

<img src="/home/akram09/Desktop/CTF-Writeups/csictf2020/web/ccc/blog_page.png" alt="home page" style="zoom:25%;" />

when we check the `/adminNames` we got a file downloaded and then redirected to the home page again the file Name was `getFile ` we opened the file and saw a strange text here is the content of the file : 

```txt
csivitu/authorized_users/blob/master/
```

we didn't understand what was that but we had a theory that it had something with **github** because of the `/blob/master` , so we continued our analysis of the website by checking the login page and as the name says we got a login form: 

<img src="/home/akram09/Desktop/CTF-Writeups/csictf2020/web/ccc/login_page.png" alt="login page" style="zoom:25%;" />

so first we checked if the forget password or the sign up but found they are fake so we tried login with dummy creds like `admin:admin` and we got redirected to the main page and saw a new cookie was added .

### deep look into login 

to get more information on how the login is working we started **BurpSuite** and  made a login with dummy creds and intercepted that request pass it to the Repeater and send the request , in result we got a token in the headers :

<img src="/home/akram09/Desktop/CTF-Writeups/csictf2020/web/ccc/login_burp.png" alt="Login Burp" style="zoom:40%;" />

by looking at the token it is for sure a `JWT TOKEN` so we need to see the content of the content and there is no better and easy way than using the [Jwt io website](https://jwt.io/)  after decoding it we got weird values in the payload even though we have use `admin:admin ` as credentials

```json
{ 
  "username": "nqzva",
  "password": "nqzva",
  "admin": "snyfr",
  "iat": 1595367508
}
```

after trying again another time with different creds we got another weird results so we knew that they were encoded  and the encoding was **ROT13** same thing with the admin key the value was false encoded with rot13, so one possible attack is signing the key with payload `admin:true ` but for that we need a secret key so we can sign our jwt token. by that we don't have something else to do so we'll just get back to the admin and look into it more deeper

### deep look into /adminNames

we got back to try our theory of that text we received being an indication of a special gituhb repository and after some search on google and github we found a github repository `https://github.com/csivitu/authorized_users` with a root directory containing a list of usernames in root folder that are 'allowed to login as root in the csivit server' as the README.md says:

```
thebongy
roerohan
namsnath
sudo-nan0-RaySK
theProgrammerDavid
sauravhiremath
```

 so first we tried all the usernames with sample password to get something or maybe get the `admin:true` but none work , so we got stuck here and we knew that we are missing something and we remembered that we haven't intercepted the request in /adminNames so after checking it in burp we found it !!:

<img src="/home/akram09/Desktop/CTF-Writeups/csictf2020/web/ccc/getAdmines_burp.png" alt="getAdmines Burp" style="zoom:40%;" />

so when we go to the `/adminNames` it redirect us to `/getFile?file=admins` so we got an LFI exploit here  and we can get any file from the server so we tried to get some files like `index.php` or `index.html` but we got file name too big  , so we can get name of a file with maximum 7 caracteres , the one file we can got is the .env file that contains useful creds, with this url `http://chall.csivit.com:30215/getFile?file=../.env`

```bash
JWT_SECRET=Th1sSECr3TMu5TN0Tb3L43KEDEv3RRRRRR!!1
```

this is the jwt secret we were looking to , it will allow us to sign our custom  jwt token 

### sign custom jwt and get flag

for this we will use [Jwt io website](https://jwt.io/)  we will sign a key we got from login with creds `thbongy:password`  and set admin to true , **NOTICE ** need rot13  and we got the token 

<img src="/home/akram09/Desktop/CTF-Writeups/csictf2020/web/ccc/jwt.png" alt="jwt token" style="zoom:25%;" />

and now we have to find where to post the token so we cheated :) and   ran a simple dirsearch on the website and got `/admin` that we haven't encoutered after sending GET request to /admin with Header `Authorization: Bearer ` to it we get the flag  `csictf{1n_th3_3nd_1t_d0esn't_3v3n_m4tt3r}` 