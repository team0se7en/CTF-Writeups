## Challenge Info 

This challenge is a HackTheBox like box,  so we are given an ip address to scan `34.93.215.188`  and  hack our way into the box , this writeups cover the challenges from Htbx02-> Htbx06 as they are the same box.

## Writeup summary

- initial enumeration 
- No Sql injection 
- XXE in /admin
- Zip Slip in /home
- Server enumeration

### Initial enumeration

As we always start with any Htb box we will launch the `nmap` scan on  the ip address `nmap -sC -sV 34.93.215.188 -oA  src/` so `-sC` is for using default nmap scripts , `-sV` for enumerating services versions , `-oA` is for output ALL format and specify the directory `src`  , NOTICE: you may be adding `-Pn` if you have an error wait for some time and here is the result : 

![nmap result ](src/nmap_result.png)

In Summary ,  we have a web application running NodeJs in port `3000` ,an  ssh port `22` and the `53` port for dns , also we should  thank  the `http.robots` nmap script  now we  have an extra information in the `robots.txt` saying there is a `/admin` route in the web application . So we will start by checking the web application at `http://34.93.215.188:3000/` :

<img src="src/website_login.png" alt="login page" style="zoom:150%;" /> 

It's a simple login form we tried dummy credentials like `admin:admin` or `admin:password` we got `No user with username: admin and password: admin.` so it actually doing the login its not just fake , first thing we tried was a sql injection attack so we tried to check if it is filtering our input by passing as credentials `';-#$()` and we got this `No user with username: ';-#$() and password: ';-#$()`  , that means it is not filtering any inputs and may be vulnerable to sql injection attacks , so we tried different payloads like `1 or 1=1`  , `1' or 1=1 --` but we had no result it keeps sending us our input , and at that moment we remembered we have a nodejs application and of course when you hear nodejs first db it came out in your mind is mongodb which is a nosql db so maybe it is a nosql injection attack lets test it out with Burpsuite.

### No Sql injection

By intercepting the request in burpsuite we can now add our payload of nosqli we used the payloads from [PayloadAllTheThings]([https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL Injection)) which is a great source for payloads , we tried the first payload `username[$ne]=toto&password[$ne]=toto` which means that the mongodb will interpret this as `username!=toto&&password&&toto` which gives true .

<img src="src/burpsuit_login.png" alt="nosql injection " style="zoom: 50%;" />

Annnddd we got redirection so nosqlinjection did work and this website is vulnerable to nosqlinjection , next thing to do when you have a vulnerable website to nosql injection is to leak the credentials and this is possible by using the regex ability in mongodb , by sending this payload `password[$regex]=m.*` mongodb will interpret this as  username start with m in regex `^m.*` so to extract information we have to make a script that bruteforce all the caracteres each at time and here is our [script](src/nosqlin.py) , wait for some time ..... and finally the creds for admin are `admin:d2f312ed7ed60ea79e3ab3d16ab2f8db` after logging with we got redirected to /home with a zip upload page 

<img src="src/zip_extract.png" alt="/home page" style="zoom:67%;" /> 

let's just check the /admin page first we got a zip extractor and by checking the source code we found the flag for **Htbx02** and here is it `csictf{n0t_4ll_1nj3ct10n5_4re_SQLi}` 

<img src="src/admin_source.png" alt="flag for htb2" style="zoom:67%;" />

 ### XXE in /admin 

by trying different payloads for each type we knew that only the json and xml were accepted in other types we receive : 

`This type is not supported right now. Sorry for the inconvenience.` so first though when we see xml we try the xml external entity `XXE` it will allow us to read files from the server so we used some payloads from [PayloadAllTheThings]([https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE Injection)) and we tried to read the /etc/passwd by using this payload we got it printed :

<img src="src/xxe_inj.png" alt="xxe injection " style="zoom:50%;" />  

So in response we got the regular `/etc/passwd` we can notice the users `csictf`, `administrator` and ... wait a minute what is that !! we found a link in the /etc/passwd to a [github gist](https://gist.github.com/sivel/c68f601137ef9063efd7)  , after reading that gist we understand it is about structuring the ssh keys for better ssh keys management , so basically for this key management to work we have to create a bash script at `/usr/local/bin/` and add our configuration to it , than we need to modify the ssh configuration to point to this bash script , so as an attacker we need to get ssh keys so we tried to read the ssh configuration with xxe `/etc/ssh/sshd_config` after a deep look into the file we saw a flag and it was for **HTBX05** `csictf{cu5t0m_4uth0rizat10n}` and after reading the`/user/local/bin/userkeys` we knew that ssh keys must be put in `/home/administrator/uploads/keys/`

<img src="src/xxe_sshd.png" alt="sshd_config" style="zoom:50%;" />

### Zip Slip in /home

after getting that flag we though we are done with the xxe attack and we must have a reverse shell or ssh keys so we tried read ssh keys from different folders but we found anything so we decided to go back to the `/home` page and scan if it has some vulnerability , so we tried to upload dummy zip it said that `zip too large` so we just put a txt dummy file in it and it returned `{success:true}` that's all , we tried to access the file we uploaded trying different routes like /file.txt , /uploads/file.txt ... but didn't found anything after a search about zip upload vulnerabilities we found a vulnerability called **ZIP SLIP** which exploit zip extraction and allow us to override files when extracting the zip .(some of the great resources to read about it are [LiveOverflow video](https://www.youtube.com/watch?v=Ry_yb5Oipq0) or [Official website](https://snyk.io/research/zip-slip-vulnerability) ), now let's create our zip exploit as this (Notice use `/home/administrator/uploads/keys/` as location to ssh public key ) 

first create the `administrator/uploads/keys` and put ssh keys in it  :

```bash
sudo mkdir -p administrator/uploads/keys
cd administrator/uploads/keys
sudo ssh-keygen 
# pass /home/administrator/uploads/keys/id_rsa  as path
```

then create our zip (NOTICE we must rename id_rsa.pub to `authorized_keys` because that's what the ssh server accept):

```bash
sudo mv id_rsa.pub authorized_keys
sudo zip exploit.zip ../../../../../../../../../../../home/administrator/uploads/keys/authorized_keys
```

we added multiple `..` because we don't know the exact path the zip will be extracted after uploading it we got `{"success":true}` let's try to connect via ssh private key 

```bash
sudo ssh -i id_rsa csictf@34.93.215.188
```

we got a shell :tada: :tada: , doing an `ls ` we dound `flag.txt` and by reading it we got a flag `csictf{w3lc0m3_t0_th3_s3rv3r}` for **HTBx03**

### Server enumeration

let's start by enumerating the /home/csictf folder 

```bash
csictf@instance-3:~$ ls -la
total 24
drwxr-xr-x 2 root root 4096 Jul 20 13:12 .
drwxr-xr-x 9 root root 4096 Jul 20 12:46 ..
-rw-r--r-- 1 root root  220 Jul 20 12:40 .bash_logout
-rw-r--r-- 1 root root 3771 Jul 20 12:40 .bashrc
-rw-r--r-- 1 root root  807 Jul 20 12:40 .profile
-rw-r--r-- 1 root root   30 Jul 20 13:12 flag.txt
```

nothing very useful here we checked the `/home` for other home directory all were empty except for the `administrator` we found two folders `uploads` where the zip where puts and `website` that contains the code for the web app , after listing and viewing different folders and files we saw a file in `website/models/db.js` that contain a flag : 

```js
csictf@instance-3:/home/administrator/website/models$ cat db.js
const mongoose = require('mongoose');

mongoose.Promise = global.Promise;

// csictf{exp0s3d_sec23ts}
mongoose.connect('mongodb://web:9EAC744765EA6F26@34.93.215.188:27017/HTBDB', {
    useNewUrlParser: true,
    useCreateIndex: true,
    useUnifiedTopology: true,
})
```

so the flag `csictf{exp0s3d_sec23ts}` is for the challenge **HTBx06**  and we have a url for connecting to mongodb with the creds in it so we tried to dump the db with `mongodump`

```bash
mongodump --uri='mongodb://web:9EAC744765EA6F26@34.93.215.188:27017/HTBDB'
```

 and we got a list of mongodb collection . after scanning the result we found the last flag for **HTBx04** in the collection stuff here is the flag `csictf{m0ng0_c0llect10ns_yay}` and that conclude this series of challenge .