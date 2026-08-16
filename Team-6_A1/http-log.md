
## JSON API Requests

</br>

- curl -v https://jsonplaceholder.typicode.com/posts/1

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host jsonplaceholder.typicode.com:443 was resolved.
* IPv6: 2606:4700:3037::ac43:a797, 2606:4700:3033::6815:3b13
* IPv4: 172.67.167.151, 104.21.59.19
*   Trying [2606:4700:3037::ac43:a797]:443...
* Connected to jsonplaceholder.typicode.com (2606:4700:3037::ac43:a797) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
} [333 bytes data]
*  CAfile: /etc/ssl/cert.pem
*  CApath: none

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* (304) (IN), TLS handshake, Server hello (2):
{ [122 bytes data]
* (304) (IN), TLS handshake, Unknown (8):
{ [19 bytes data]
* (304) (IN), TLS handshake, Certificate (11):
{ [2490 bytes data]
* (304) (IN), TLS handshake, CERT verify (15):
{ [79 bytes data]
* (304) (IN), TLS handshake, Finished (20):
{ [36 bytes data]
* (304) (OUT), TLS handshake, Finished (20):
} [36 bytes data]
* SSL connection using TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256 / [blank] / UNDEF
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=typicode.com
*  start date: Jul 29 23:06:19 2026 GMT
*  expire date: Oct 28 00:04:44 2026 GMT
*  subjectAltName: host "jsonplaceholder.typicode.com" matched cert's "*.typicode.com"
*  issuer: C=US; O=Google Trust Services; CN=WE1
*  SSL certificate verify ok.
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://jsonplaceholder.typicode.com/posts/1
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: jsonplaceholder.typicode.com]
* [HTTP/2] [1] [:path: /posts/1]
* [HTTP/2] [1] [user-agent: curl/8.7.1]
* [HTTP/2] [1] [accept: */*]
> GET /posts/1 HTTP/2
> Host: jsonplaceholder.typicode.com
> User-Agent: curl/8.7.1
> Accept: */*
> 
* Request completely sent off
< HTTP/2 200 
< date: Sat, 15 Aug 2026 17:36:33 GMT
< content-type: application/json; charset=utf-8
< content-length: 292
< access-control-allow-credentials: true
< cache-control: max-age=43200
< etag: W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"
< expires: -1
< nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
< pragma: no-cache
< report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=PD3aZ5JXmnXLLbuM9yuy2jwg6ke8U5C2Yq%2BT0erzkj0%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1775729378"}],"max_age":3600}
< reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=PD3aZ5JXmnXLLbuM9yuy2jwg6ke8U5C2Yq%2BT0erzkj0%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1775729378"
< server: cloudflare
< vary: Origin, Accept-Encoding
< via: 2.0 heroku-router
< x-content-type-options: nosniff
< x-powered-by: Express
< x-ratelimit-limit: 1000
< x-ratelimit-remaining: 730
< x-ratelimit-reset: 1775729393
< age: 4275
< accept-ranges: bytes
< cf-cache-status: HIT
< cf-ray: a2b9f64d4939c390-SIN
< alt-svc: h3=":443"; ma=86400
< 

  0   292    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0{ [292 bytes data]

100   292  100   292    0     0    249      0  0:00:01  0:00:01 --:--:--   249
* Connection #0 to host jsonplaceholder.typicode.com left intact
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

</br>

- curl -v https://jsonplaceholder.typicode.com/users/9

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host jsonplaceholder.typicode.com:443 was resolved.
* IPv6: 2606:4700:3033::6815:3b13, 2606:4700:3037::ac43:a797
* IPv4: 172.67.167.151, 104.21.59.19
*   Trying [2606:4700:3033::6815:3b13]:443...
* Connected to jsonplaceholder.typicode.com (2606:4700:3033::6815:3b13) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
} [333 bytes data]
*  CAfile: /etc/ssl/cert.pem
*  CApath: none
* (304) (IN), TLS handshake, Server hello (2):
{ [122 bytes data]
* (304) (IN), TLS handshake, Unknown (8):
{ [19 bytes data]
* (304) (IN), TLS handshake, Certificate (11):
{ [2490 bytes data]
* (304) (IN), TLS handshake, CERT verify (15):
{ [79 bytes data]
* (304) (IN), TLS handshake, Finished (20):
{ [36 bytes data]
* (304) (OUT), TLS handshake, Finished (20):
} [36 bytes data]
* SSL connection using TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256 / [blank] / UNDEF
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=typicode.com
*  start date: Jul 29 23:06:19 2026 GMT
*  expire date: Oct 28 00:04:44 2026 GMT
*  subjectAltName: host "jsonplaceholder.typicode.com" matched cert's "*.typicode.com"
*  issuer: C=US; O=Google Trust Services; CN=WE1
*  SSL certificate verify ok.
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://jsonplaceholder.typicode.com/users/9
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: jsonplaceholder.typicode.com]
* [HTTP/2] [1] [:path: /users/9]
* [HTTP/2] [1] [user-agent: curl/8.7.1]
* [HTTP/2] [1] [accept: */*]
> GET /users/9 HTTP/2
> Host: jsonplaceholder.typicode.com
> User-Agent: curl/8.7.1
> Accept: */*
> 
* Request completely sent off
< HTTP/2 200 
< date: Sat, 15 Aug 2026 17:36:33 GMT
< content-type: application/json; charset=utf-8
< content-length: 523
< access-control-allow-credentials: true
< cache-control: max-age=43200
< etag: W/"20b-s6q9RrZIuKoibQPA95Vsu2dPF/s"
< expires: -1
< nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
< pragma: no-cache
< report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=ky%2FKe8SXgFxM85aWOWEBA2DJ86t0u5MtMRxLbEv9qJM%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785384018"}],"max_age":3600}
< reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=ky%2FKe8SXgFxM85aWOWEBA2DJ86t0u5MtMRxLbEv9qJM%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785384018"
< server: cloudflare
< vary: Origin, Accept-Encoding
< via: 2.0 heroku-router
< x-content-type-options: nosniff
< x-powered-by: Express
< x-ratelimit-limit: 1000
< x-ratelimit-remaining: 999
< x-ratelimit-reset: 1785384036
< age: 21376
< accept-ranges: bytes
< cf-cache-status: HIT
< cf-ray: a2b9f65419f26656-AMS
< alt-svc: h3=":443"; ma=86400
< 
{ [523 bytes data]

100   523  100   523    0     0   1126      0 --:--:-- --:--:-- --:--:--  1127
* Connection #0 to host jsonplaceholder.typicode.com left intact
{
  "id": 9,
  "name": "Glenna Reichert",
  "username": "Delphine",
  "email": "Chaim_McDermott@dana.io",
  "address": {
    "street": "Dayna Park",
    "suite": "Suite 449",
    "city": "Bartholomebury",
    "zipcode": "76495-3109",
    "geo": {
      "lat": "24.6463",
      "lng": "-168.8889"
    }
  },
  "phone": "(775)976-6794 x41206",
  "website": "conrad.com",
  "company": {
    "name": "Yost and Sons",
    "catchPhrase": "Switchable contextually-based project",
    "bs": "aggregate real-time technologies"
  }
}
```

</br>

- curl -v -X POST https://jsonplaceholder.typicode.com/posts -H "Content-Type: application/json" -d '{"title":"TeamID-6"}'

```
Note: Unnecessary use of -X or --request, POST is already inferred.
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host jsonplaceholder.typicode.com:443 was resolved.
* IPv6: 2606:4700:3037::ac43:a797, 2606:4700:3033::6815:3b13
* IPv4: 172.67.167.151, 104.21.59.19
*   Trying [2606:4700:3037::ac43:a797]:443...
* Connected to jsonplaceholder.typicode.com (2606:4700:3037::ac43:a797) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
} [333 bytes data]
*  CAfile: /etc/ssl/cert.pem
*  CApath: none
* (304) (IN), TLS handshake, Server hello (2):
{ [122 bytes data]
* (304) (IN), TLS handshake, Unknown (8):
{ [19 bytes data]
* (304) (IN), TLS handshake, Certificate (11):
{ [2490 bytes data]
* (304) (IN), TLS handshake, CERT verify (15):
{ [78 bytes data]
* (304) (IN), TLS handshake, Finished (20):
{ [36 bytes data]
* (304) (OUT), TLS handshake, Finished (20):
} [36 bytes data]
* SSL connection using TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256 / [blank] / UNDEF
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=typicode.com
*  start date: Jul 29 23:06:19 2026 GMT
*  expire date: Oct 28 00:04:44 2026 GMT
*  subjectAltName: host "jsonplaceholder.typicode.com" matched cert's "*.typicode.com"
*  issuer: C=US; O=Google Trust Services; CN=WE1
*  SSL certificate verify ok.
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://jsonplaceholder.typicode.com/posts
* [HTTP/2] [1] [:method: POST]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: jsonplaceholder.typicode.com]
* [HTTP/2] [1] [:path: /posts]
* [HTTP/2] [1] [user-agent: curl/8.7.1]
* [HTTP/2] [1] [accept: */*]
* [HTTP/2] [1] [content-type: application/json]
* [HTTP/2] [1] [content-length: 20]
> POST /posts HTTP/2
> Host: jsonplaceholder.typicode.com
> User-Agent: curl/8.7.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 20
> 
} [20 bytes data]
* upload completely sent off: 20 bytes
< HTTP/2 201 
< date: Sat, 15 Aug 2026 17:36:34 GMT
< content-type: application/json; charset=utf-8
< content-length: 38
< location: https://jsonplaceholder.typicode.com/posts/101
< access-control-allow-credentials: true
< access-control-expose-headers: Location
< cache-control: no-cache
< etag: W/"26-SU4KBTJjGI71vvCx4Y5eEbVoYAk"
< expires: -1
< nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
< pragma: no-cache
< report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=Tulg5foMlnJtwu2EQ0PjJD7wLAwEf2w3DovhYTI2UJM%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786815394"}],"max_age":3600}
< reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=Tulg5foMlnJtwu2EQ0PjJD7wLAwEf2w3DovhYTI2UJM%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786815394"
< server: cloudflare
< vary: Origin, X-HTTP-Method-Override, Accept-Encoding
< via: 2.0 heroku-router
< x-content-type-options: nosniff
< x-powered-by: Express
< x-ratelimit-limit: 1000
< x-ratelimit-remaining: 999
< x-ratelimit-reset: 1786815403
< cf-cache-status: DYNAMIC
< cf-ray: a2b9f6564eb1ce31-SIN
< alt-svc: h3=":443"; ma=86400
< 
{ [38 bytes data]

100    58  100    38  100    20     78     41 --:--:-- --:--:-- --:--:--   119
100    58  100    38  100    20     78     41 --:--:-- --:--:-- --:--:--   119
* Connection #0 to host jsonplaceholder.typicode.com left intact
{
  "title": "TeamID-6",
  "id": 101
}
```

</br>

- curl -v https://jsonplaceholder.typicode.com/posts/9999

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host jsonplaceholder.typicode.com:443 was resolved.
* IPv6: 2606:4700:3037::ac43:a797, 2606:4700:3033::6815:3b13
* IPv4: 172.67.167.151, 104.21.59.19
*   Trying [2606:4700:3037::ac43:a797]:443...
* Connected to jsonplaceholder.typicode.com (2606:4700:3037::ac43:a797) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
} [333 bytes data]
*  CAfile: /etc/ssl/cert.pem
*  CApath: none
* (304) (IN), TLS handshake, Server hello (2):
{ [122 bytes data]
* (304) (IN), TLS handshake, Unknown (8):
{ [19 bytes data]
* (304) (IN), TLS handshake, Certificate (11):
{ [2490 bytes data]
* (304) (IN), TLS handshake, CERT verify (15):
{ [80 bytes data]
* (304) (IN), TLS handshake, Finished (20):
{ [36 bytes data]
* (304) (OUT), TLS handshake, Finished (20):
} [36 bytes data]
* SSL connection using TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256 / [blank] / UNDEF
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=typicode.com
*  start date: Jul 29 23:06:19 2026 GMT
*  expire date: Oct 28 00:04:44 2026 GMT
*  subjectAltName: host "jsonplaceholder.typicode.com" matched cert's "*.typicode.com"
*  issuer: C=US; O=Google Trust Services; CN=WE1
*  SSL certificate verify ok.
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://jsonplaceholder.typicode.com/posts/9999
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: jsonplaceholder.typicode.com]
* [HTTP/2] [1] [:path: /posts/9999]
* [HTTP/2] [1] [user-agent: curl/8.7.1]
* [HTTP/2] [1] [accept: */*]
> GET /posts/9999 HTTP/2
> Host: jsonplaceholder.typicode.com
> User-Agent: curl/8.7.1
> Accept: */*
> 
* Request completely sent off
< HTTP/2 404 
< date: Sat, 15 Aug 2026 17:36:35 GMT
< content-type: application/json; charset=utf-8
< content-length: 2
< access-control-allow-credentials: true
< cache-control: max-age=43200
< etag: W/"2-vyGp6PvFo4RvsFtPoIWeCReyIC8"
< expires: -1
< nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
< pragma: no-cache
< report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=JWdPa5LuslCnQ0G2DhTNJ0PJQJVzMLTQm2VUd4YubPo%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786793904"}],"max_age":3600}
< reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=JWdPa5LuslCnQ0G2DhTNJ0PJQJVzMLTQm2VUd4YubPo%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786793904"
< server: cloudflare
< vary: Origin, Accept-Encoding
< via: 2.0 heroku-router
< x-content-type-options: nosniff
< x-powered-by: Express
< x-ratelimit-limit: 1000
< x-ratelimit-remaining: 999
< x-ratelimit-reset: 1786793923
< age: 21491
< cf-cache-status: HIT
< cf-ray: a2b9f65abc495914-SIN
< alt-svc: h3=":443"; ma=86400
< 
{ [2 bytes data]

100     2  100     2    0     0      1      0  0:00:02  0:00:01  0:00:01     1
100     2  100     2    0     0      1      0  0:00:02  0:00:01  0:00:01     1
* Connection #0 to host jsonplaceholder.typicode.com left intact
{}
```

</br>

- curl -v https://jsonplaceholder.typicode.com/iiitv/assignments/1

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host jsonplaceholder.typicode.com:443 was resolved.
* IPv6: 2606:4700:3037::ac43:a797, 2606:4700:3033::6815:3b13
* IPv4: 104.21.59.19, 172.67.167.151
*   Trying [2606:4700:3037::ac43:a797]:443...
* Connected to jsonplaceholder.typicode.com (2606:4700:3037::ac43:a797) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
} [333 bytes data]
*  CAfile: /etc/ssl/cert.pem
*  CApath: none
* (304) (IN), TLS handshake, Server hello (2):
{ [122 bytes data]

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* (304) (IN), TLS handshake, Unknown (8):
{ [19 bytes data]
* (304) (IN), TLS handshake, Certificate (11):
{ [2490 bytes data]
* (304) (IN), TLS handshake, CERT verify (15):
{ [79 bytes data]
* (304) (IN), TLS handshake, Finished (20):
{ [36 bytes data]
* (304) (OUT), TLS handshake, Finished (20):
} [36 bytes data]
* SSL connection using TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256 / [blank] / UNDEF
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=typicode.com
*  start date: Jul 29 23:06:19 2026 GMT
*  expire date: Oct 28 00:04:44 2026 GMT
*  subjectAltName: host "jsonplaceholder.typicode.com" matched cert's "*.typicode.com"
*  issuer: C=US; O=Google Trust Services; CN=WE1
*  SSL certificate verify ok.
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://jsonplaceholder.typicode.com/iiitv/assignments/1
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: jsonplaceholder.typicode.com]
* [HTTP/2] [1] [:path: /iiitv/assignments/1]
* [HTTP/2] [1] [user-agent: curl/8.7.1]
* [HTTP/2] [1] [accept: */*]
> GET /iiitv/assignments/1 HTTP/2
> Host: jsonplaceholder.typicode.com
> User-Agent: curl/8.7.1
> Accept: */*
> 
* Request completely sent off
< HTTP/2 404 
< date: Sat, 15 Aug 2026 17:50:36 GMT
< content-type: application/json; charset=utf-8
< content-length: 2
< access-control-allow-credentials: true
< cache-control: max-age=43200
< etag: W/"2-vyGp6PvFo4RvsFtPoIWeCReyIC8"
< expires: -1
< nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
< pragma: no-cache
< report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=R3NM0CS9Q8gW%2FMnvtNMH0tAvR72lLJG61vEnQp%2FXgqA%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786816236"}],"max_age":3600}
< reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=R3NM0CS9Q8gW%2FMnvtNMH0tAvR72lLJG61vEnQp%2FXgqA%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786816236"
< server: cloudflare
< vary: Origin, Accept-Encoding
< via: 2.0 heroku-router
< x-content-type-options: nosniff
< x-powered-by: Express
< x-ratelimit-limit: 1000
< x-ratelimit-remaining: 999
< x-ratelimit-reset: 1786816243
< cf-cache-status: MISS
< cf-ray: a2ba0ae0aa50ce66-SIN
< alt-svc: h3=":443"; ma=86400
< 
{ [2 bytes data]

100     2  100     2    0     0      1      0  0:00:02  0:00:01  0:00:01     1
100     2  100     2    0     0      1      0  0:00:02  0:00:01  0:00:01     1
* Connection #0 to host jsonplaceholder.typicode.com left intact
{}
```


</br> </br>

## Status Codes

<b>200</b> : The Request was successful and the server returned the desired response.
</br>
<b>201</b> : The Request was successful and the server created a new item that we requested.
</br>
<b>404</b> : Client requested for a resource that doesn't exists or the server couldn't find it.


</br> </br>

## Content Type

<b>application / json</b> : This means that the response body is JSON formatted text, encoded using UTF-8
