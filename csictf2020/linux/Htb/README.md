## Challenge Info 

This challenge is a HackTheBox like box,  so we are given an ip address to scan `34.93.215.188`  and  hack our way into the box , this writeups cover the challenges from Htbx02-> Htbx06 as they are the same box.

## Writeup summary

- initial enumeration 
- No Sql injection 
- XXE in /admin

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

<img src="/home/akram09/Desktop/CTF-Writeups/csictf2020/linux/Htb/src/zip_extract.png" alt="/home page" style="zoom:67%;" /> 

let's just check the /admin page first we got a zip extractor and by checking the source code we found the flag for **Htbx02** and here is it `csictf{n0t_4ll_1nj3ct10n5_4re_SQLi}` 

<img src="/home/akram09/Desktop/CTF-Writeups/csictf2020/linux/Htb/src/admin_source.png" alt="flag for htb2" style="zoom:67%;" />

 ### XXE in /admin 

by trying different payloads for each type we knew that only the json and xml were accepted in other types we receive : 

`This type is not supported right now. Sorry for the inconvenience.` so first though when we see xml we try the xml external entity `XXE` it will allow us to read files from the server so we used some payloads from [PayloadAllTheThings]([https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE Injection)) and we tried to read the /etc/passwd by using this payload we got it printed :

<img src="src/xxe_inj.png" alt="xxe injection " style="zoom:50%;" />  

So in response we got the regular `/etc/passwd` we can notice the users `csictf`, `administrator` and ... wait a minute what is that !! we found a link in the /etc/passwd to a [github gist](https://gist.github.com/sivel/c68f601137ef9063efd7)  , after reading that gist we understand it is about structuring the ssh keys for better ssh keys management , so basically for this key management to work we have to create a bash script at `/usr/local/bin/` and add our configuration to it , than we need to modify the ssh configuration to point to this bash script , so as an attacker we need to get ssh keys so we tried to read the ssh configuration with xxe `/etc/ssh/sshd_config` after a deep look into the file we saw a flag and it was for **HTBX05** `csictf{cu5t0m_4uth0rizat10n}`

<img src="/home/akram09/Desktop/CTF-Writeups/csictf2020/linux/Htb/src/xxe_sshd.png" alt="sshd_config" style="zoom:50%;" />