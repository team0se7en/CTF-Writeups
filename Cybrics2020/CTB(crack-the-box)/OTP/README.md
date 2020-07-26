## Challenge Info

A crack the box challenge (hackthebox/vulnhub-like) `http://otp-cybrics2020.ctf.su/` the web-page provides a input for auth token and a the client binary and the server's, and the source code of the server.
<img src="src/webpage.png" alt="page" style="zoom:25%;" />

## TL-DR 

We discover the client binary is using ssh, we get the private key out of the binary and get the user also we use ssh keys to do forward port tunneling of the mongodb port from the server to our machine we connect to the db and get the otp of the admin provide it to the website and we get the flag.

## Writeup Summary

- Understanding how the service works.
- Doing some blackbox analyses on the client binary.
- Port forwarding the mongodb port to our machine.
- Getting the otp from the mongodb and submitting it to get the flag.

### Initial Understanding

The client binary can be used to login or register an account, the login mechanism do it's magic and get u a token :

```
./client login -l user7 -p userpass7
Response: SUCCESS: ac003f82-edfc-4855-b761-bdc59406d8d4
```

The token can be submitted into the webpage but get nothing because we're not admin:

<img src="src/not_admin.png" alt="page" style="zoom:25%;" />

 that means the admin token is the target.
The server binary we can understand it's functionality from the source code, It's expect 3 lines as input, first one is the action(login/register), the second is username, the third is password; It connects to a mongodb and create a user in case of register or verify the creds and create an otp in case of login.
PS: the server's code import mongodb configs (username,pass, host,port) from a .env file but still uses hardcoded creds, dbname and collection.

### Blackbox Analyses

Both the client and the server were written in go, we first tried reverse engineering it but we all know how messy that can be, so we tried some black box analyses, First we analyzed the network using strace : `strace -f -e trace=network ./client login -l user7 -p userpass7` 

<img src="src/strace.png" alt="page" style="zoom:25%;" />

We see the client app resolves the domain `otp-cybrics2020.ctf.su` and gets it's ip address `34.76.112.206` but we can't get how the data is sent, so we decide to capture the network sent to that specific ip, we used tcpdump : `tcpdump -i wlp7s0 dst 34.76.112.206 -w Capture.pcap`

Taking a look at the capture with wireshark:

<img src="src/wireshark.png" alt="page" style="zoom:25%;" />

We confirmed the app is using ssh but we have no creds or ssh keys since the packets are encrypted, running strings on the app and greping for specific patterns we got ssh private keys [id_rsa](src/id_rsa)

We need a username now, we tried guessing nothing came out, To try and get the username we modified out `/etc/hosts` so the challenge domain points back to our loopback address `127.0.0.1` we run the binary and the we check our ssh logs with: `systemctl status sshd`
we got : `sshd[13342]: Invalid user guest from 127.0.0.1 port 40898`

The user is guest, I guess our guess work wasn't on point :stuck_out_tongue: .

Now we got everything for the ssh connection.

### SSH session 

Connection to the ssh session we don't get a shell but instead a clear prompt, poking at it a little we know it's the server's binary, we don't get much, but it's ssh and ssh has many features builtin on it, one of many is port forwarding (more on port forwarding over [here](https://www.ssh.com/ssh/tunneling/example) ), we port forward the mongodb port 27017 since we already got the creds from the source code of the server.
`ssh -L 27017:localhost:27017 guest@34.76.112.206 -i id_rsa`

Checking open port on our machine and:
`tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      9530/ssh` 
It's open.

### Connecting to mongodb

Since we already have the creds `mongodb://admin:admin@localhost:27017` and the db name `cybrics` (Both from the source code).
We can connect right to the db away : `mongo -u admin -p admin --authenticationDatabase cybrics`

We already know the schema from the source so we right away query the admin user

```
> use cybrics
switched to db cybrics
> db
cybrics
> db.users.find({username : "admin"})
{ "_id" : ObjectId("5f1ae2e97e2bd0263657b0ee"), "username" : "admin", "password" : "j77d32g72373ggasdkasdGG&SD", "otp" : "f41a137f-aeb0-4518-9d20-2aafc4fcb90f" }
>
```

We get the admin's otp : `f41a137f-aeb0-4518-9d20-2aafc4fcb90f`
We submit it in the web to get the flag:

<img src="src/flag.png" alt="page" style="zoom:25%;" />

Flag: `cybrics{n07_S0_D1fF1cuL7_8U7_4lw4yS_chECK_P0R7_F0rw4Rd1N9}`

