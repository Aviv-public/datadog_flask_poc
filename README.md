# DATADOG Flask poc

```bash
$ DD_API_KEY=xxx docker-compose up
```

Generate HTTP 500 Error
```bash
$ curl http://localhost:5000/raise
```

```html
<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
```