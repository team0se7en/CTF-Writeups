# Whois

## Description:

> Tags: medium

> A web-based Whois service

> Author : souad

> https://whois.challs.shellmates.club

## First thoughts:

This is a wab challenge. Checking the website, we find that it asks for a link, Whois server and it returns the result of running whois with those parameters.

## Testing and discovering:

The first thing I noticed was that the placeholder for the url input said `php.net`, so must likely the website is written in php.

Entering a website and submitting the form redirects us to another end-point:
```
https://whois.challs.shellmates.club/query.php?host=whois.verisign-grs.com&query=php.net
```
so now we know that the application at least has two pages:
 - index.php
 - query.php

The next thing I thought about was changing the type of input (kinda), from the parameters, we know that both are sent as strings, what if we change one of them and make it an array ?

> Note: to send an array of elements to php, we add `[]` to a parameter's name.

So I tried :
```
https://whois.challs.shellmates.club/query.php?host[]=whois.verisign-grs.com&query=php.net
```

and here is what I got:

```php
<?php

error_reporting(0);

$output = null;
$host_regex = "/^[0-9a-zA-Z][0-9a-zA-Z\.-]+$/";
$query_regex = "/^[0-9a-zA-Z\. ]+$/";


if (isset($_GET['query']) && isset($_GET['host']) && 
      is_string($_GET['query']) && is_string($_GET['host'])) {

  $query = $_GET['query'];
  $host = $_GET['host'];
  
  if ( !preg_match($host_regex, $host) || !preg_match($query_regex, $query) ) {
    $output = "Invalid query or whois host";
  } else {
    $output = shell_exec("/usr/bin/whois -h ${host} ${query}");
  }

} 
else {
  highlight_file(__FILE__);
  exit;
}

?>

<!DOCTYPE html>
<html>
  <head>
    <title>Whois</title>
  </head>
  <body>
    <pre><?= htmlspecialchars($output) ?></pre>
  </body>
</html>
```

So let's have a list of the things we can get from this code:

 - Our input is tested if it exists and if it is a string:
    - If no: the file is returned.
    - If yes: 
        - Our input is tested against a regex and if one of the tests fails, it returns `Invalid query or whois host`, else it executes `/usr/bin/whois -h ${host} ${query`.

So now, if we try to display the page `query.php` without any parameters, it should return the source code of the page.

## Stupid Simple idea came to my mind:

If we could access `query.php` and get its source code, what would happen if we try accessing
```
https://whois.challs.shellmates.club/flag.txt
```

Oh no, we got the flag:
```
shellmates{i_$h0U1D_HaVE_R3AD_7HE_dOc_W3Ll}
```

Wait, but which Doc? I asked the creator of the challenge about the way I solved the challenge and she confirmed that it's an unintended solution, the server was misconfigured and the flag.txt file wasn't hidden.

## So what is the real solution ?

Check [Whois-fixed](../Whois_fixed/)